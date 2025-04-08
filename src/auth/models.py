from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class User(Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String, primary_key=True)
    email: Mapped[str | None] = mapped_column(String, unique=True)
    full_name: Mapped[str | None] = mapped_column(String)
    hashed_password: Mapped[str] = mapped_column(String)
    disabled: Mapped[bool] = mapped_column(Boolean, default=False)

    def __repr__(self):
        return (
            f"<User("
            f"username={self.username!r}, "
            f"email={self.email!r}, "
            f"full_name={self.full_name!r}, "
            f"disabled={self.disabled!r}"
            f")>"
        )


class Token(Base):
    __tablename__ = "tokens"

    access_token: Mapped[str] = mapped_column(String, primary_key=True)
    token_type: Mapped[str] = mapped_column(String)

    def __repr__(self):
        return (
            f"<Token("
            f"access_token={self.access_token!r}, "
            f"token_type={self.token_type!r}"
            f")>"
        )
