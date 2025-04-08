from fastapi import APIRouter, HTTPException, status

from src.auth.dependencies import CurrentUser, DBSession, OAuth2Form
from src.auth.schemas import Token as TokenSchema
from src.auth.schemas import User as UserSchema
from src.auth.schemas import UserCreate
from src.auth.services import create_user, get_token

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(db: DBSession, req_user: UserCreate):
    created = create_user(db, req_user)

    if not created:
        raise HTTPException(status_code=409, detail="Username already exists")
    return {"message": "User created"}


@router.post("/login")
async def login(
    db: DBSession,
    form_data: OAuth2Form,
) -> TokenSchema:
    return get_token(db, form_data.username, form_data.password)


@router.get("/users/me", response_model=UserSchema)
async def read_users_me(current_user: CurrentUser):
    user = UserSchema(**current_user.__dict__)
    return user
