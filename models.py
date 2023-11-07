from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, DateTime, func, Integer
from datetime import datetime


POSTGRES_DSN = f"postgresql://app:1234@127.0.0.1:5432/app"

engine = create_engine(POSTGRES_DSN)
Session = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


class Message(Base):

    __tablename__ = 'app_message'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    creation_date: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    description: Mapped[str] = mapped_column(String(400), nullable=False)
    creator: Mapped[str] = mapped_column(String(20), nullable=False)


Base.metadata.create_all(bind=engine)