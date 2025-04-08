from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from src.config import settings


class Base(DeclarativeBase):
    pass


sync_engine = create_engine(settings.database_url)

Base.metadata.create_all(bind=sync_engine)

SessionLocal = sessionmaker(bind=sync_engine)


def get_db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
