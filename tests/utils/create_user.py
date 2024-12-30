from sqlalchemy.orm import Session

from app.auth.utils import security
from app.users.repositories.users_repository import users_repository
from app.users.schemas.user_schema import UserCreate, UserInDB
from app.users.services.users_service import UsersService


def create_user(
    session: Session,
) -> UserInDB:
    hashed_password = security.get_password_hash("password")
    new_user = UserCreate(
        email="test@user.com", hashed_password=hashed_password
    )
    return UsersService(session, users_repository).create_user(new_user)
