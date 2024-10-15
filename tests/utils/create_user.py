from sqlalchemy.orm import Session

from app.core import security
from app.repositories.users_repository import users_repository
from app.schemas.user_schema import UserCreate, UserInDBBase
from app.services.users_service import UsersService


def create_user(
    session: Session,
) -> UserInDBBase:
    hashed_password = security.get_password_hash("password")
    new_user = UserCreate(
        email="test@user.com", hashed_password=hashed_password
    )
    return UsersService(session, users_repository).create_user(new_user)
