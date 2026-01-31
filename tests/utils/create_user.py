from sqlalchemy.orm import Session

from app.auth.utils import security
from app.users.domain.user_dtos import UserCreate
from app.users.domain.user_dtos import UserInDB
from app.users.services.users_service import UsersService


def create_user(
    session: Session,
) -> UserInDB:
    hashed_password = security.get_password_hash("password")
    new_user = UserCreate(
        email="test@user.com", hashed_password=hashed_password
    )
    return UsersService(session).create_user(new_user)
