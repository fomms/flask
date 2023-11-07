import pydantic


class CreateMessage(pydantic.BaseModel):
    title: str
    description: str
    creator: str

    @pydantic.field_validator("title")
    @classmethod
    def check_title(cls, v):
        if len(v) > 50:
            raise ValueError(f'Maximum length of title is 50')
        return v


    @pydantic.field_validator("description")
    @classmethod
    def check_description(cls, v):
        if len(v) > 400:
            raise ValueError(f'Maximum length of description is 400')
        return v

    @pydantic.field_validator("creator")
    @classmethod
    def check_creator(cls, v):
        if len(v) > 20:
            raise ValueError(f'Maximum length of creator is 20')
        return v