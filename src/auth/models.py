from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class UserModel(Base):
    username: Mapped[str] = mapped_column(String, primary_key=True)
    email: Mapped[str | None] = mapped_column(String, unique=True)
    full_name: Mapped[str | None] = mapped_column(String)
    disabled: Mapped[bool] = mapped_column(Boolean, default=False)
    hashed_password: Mapped[str] = mapped_column(String)


class TokenModel(Base):
    access_token: Mapped[str] = mapped_column(String, primary_key=True)
    token_type: Mapped[str] = mapped_column(String)
