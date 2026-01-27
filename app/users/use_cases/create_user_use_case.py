from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from app.auth.utils import security
from app.emails.services.emails_service import EmailService
from app.users.schemas.user_schema import (
    CreateUserRequest,
    UserCreate,
    UserResponse,
)
from app.users.services.users_service import UsersService


class CreateUserUseCase:
    def __init__(self, session: Session):
        self.session = session

    def execute(self, create_user_request: CreateUserRequest) -> UserResponse:
        users_service = UsersService(self.session)
        if users_service.get_by_email(create_user_request.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with that email already registered.",
            )

        created_user = users_service.create_user(
            UserCreate(
                email=create_user_request.email.lower(),
                hashed_password=security.get_password_hash(
                    create_user_request.password
                ),
            )
        )

        EmailService().send_new_user_email(created_user)

        return UserResponse(
            id=created_user.id,
            email=created_user.email,
        )
