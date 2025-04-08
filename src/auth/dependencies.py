from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from src.auth.models import User
from src.auth.services import get_current_active_user
from src.database import DBSession

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
TokenScheme = Annotated[str, Depends(oauth2_scheme)]
OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]


def current_user(db: DBSession, token: TokenScheme):
    db_user = get_current_active_user(db, token)
    return db_user


CurrentUser = Annotated[User, Depends(current_user)]
