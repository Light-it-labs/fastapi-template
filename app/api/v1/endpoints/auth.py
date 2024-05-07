from fastapi import APIRouter, HTTPException

from app.api.dependencies.get_db import SessionDependency
from app.core.config import get_settings
from app.core.security import create_access_token
from app.repositories.users_repository import users_repository
from app.schemas.auth_schema import UserLogin
from app.schemas.token_schema import Token, TokenPayload
from app.services.auth_service import AuthService

router = APIRouter()
settings = get_settings()


@router.post("/login")
def login_access_token(session: SessionDependency, login_data: UserLogin) -> Token:
    user = AuthService(session, users_repository).authenticate(
        email=login_data.email, password=login_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    return Token(access_token=create_access_token(TokenPayload(user_id=str(user.id))))
