from datetime import timedelta

from jwt import InvalidTokenError
from sqlalchemy.orm import Session

from src.auth.exceptions import (
    CredentialsException,
    InactiveUserException,
    IncorrectCredentialsException,
)
from src.auth.models import Token, User
from src.auth.schemas import TokenData
from src.auth.schemas import User as UserSchema
from src.auth.utils import (
    create_access_token,
    decode_token,
    get_password_hash,
    verify_password,
)
from src.config import settings


def create_user(db: Session, req_user: UserSchema) -> bool:
    db_user = db.query(User).filter(User.username == req_user.username).first()

    if db_user is not None:
        return False

    new_user = User(
        username=req_user.username,
        email=req_user.email,
        full_name=req_user.full_name,
        hashed_password=get_password_hash(req_user.password),
        disabled=False,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return True


def get_user(db: Session, username: str):
    user = db.query(User).filter(User.username == username).first()
    return user if user else None


def get_current_user(db: Session, token: str):
    try:
        payload = decode_token(token)
        username = payload.get("sub")
        if username is None:
            raise CredentialsException()
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise CredentialsException()
    user = get_user(db, username=token_data.username)
    if user is None:
        raise CredentialsException()
    return user


def get_current_active_user(db: Session, token: str):
    current_user = get_current_user(db, token)
    if current_user.disabled:
        raise InactiveUserException
    return current_user


def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def get_token(db: Session, username: str, password: str) -> Token:
    user = authenticate_user(db, username, password)
    if not user:
        raise IncorrectCredentialsException()
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
