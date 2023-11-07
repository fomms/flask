import flask
from flask import jsonify, request, Response
from flask.views import MethodView
from models import Session, Message
from pydantic import ValidationError
from schema import CreateMessage

app = flask.Flask('app')


class HttpError(Exception):
    def __init__(self, status_code: int, description: str):
        self.status_code = status_code
        self.description = description


@app.errorhandler(HttpError)
def error_handler(error):
    response = jsonify({"error": error.description})
    response.status_code = error.status_code
    return response


@app.before_request
def before_request():
    session = Session()
    request.session = session


@app.after_request
def after_request(response: Response):
    request.session.close()
    return response


def get_message(message_id: int):
    message = request.session.get(Message, message_id)
    if message is None:
        raise HttpError(404, "message not found")
    return message


def validate(model, data):
    try:
        return model.model_validate(data).model_dump()
    except ValidationError as err:
        error = err.errors()[0]
        error.pop("ctx", None)
        raise HttpError(400, error)

class MessageView(MethodView):

    @property
    def session(self) -> Session:
        return request.session

    def get(self, message_id: int):
        message = get_message(message_id)
        return jsonify({"id": message.id, "title": message.title, "creation_date": message.creation_date.isoformat(),
                        "description": message.description, "creator": message.creator})

    def post(self):
        message_data = validate(CreateMessage, request.json)
        new_message = Message(**message_data)
        request.session.add(new_message)
        request.session.commit()
        return jsonify({"id": new_message.id})

    def delete(self, message_id: int):
        message = get_message(message_id)
        self.session.delete(message)
        self.session.commit()
        return jsonify({"status": "message deleted"})


message_view = MessageView.as_view('message_view')
app.add_url_rule(rule='/message/<int:message_id>', view_func=message_view, methods=['GET', 'DELETE'])
app.add_url_rule(rule='/message', view_func=message_view, methods=['POST'])


if __name__ == '__main__':
    app.run(debug=True)