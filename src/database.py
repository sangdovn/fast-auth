from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from src.config import settings


class Base(DeclarativeBase):
    pass


sync_engine = create_engine(settings.database_url)
SessionFactory = sessionmaker(bind=sync_engine, autoflush=False, expire_on_commit=False)


def init_db():
    Base.metadata.create_all(bind=sync_engine)


def get_db():
    session = SessionFactory()
    try:
        yield session
    finally:
        session.close()


DBSession = Annotated[Session, Depends(get_db)]
