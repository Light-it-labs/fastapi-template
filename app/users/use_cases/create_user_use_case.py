from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from fastapi import status

from app.auth.utils import security
from app.users.repositories.users_repository import users_repository
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
        from app.celery.tasks.emails import send_welcome_email

        users_service = UsersService(self.session, users_repository)
        if users_service.get_by_email(create_user_request.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with that email already registered.",
            )

        created_user = UsersService(
            self.session, users_repository
        ).create_user(
            UserCreate(
                email=create_user_request.email,
                hashed_password=security.get_password_hash(
                    create_user_request.password
                ),
            )
        )

        send_welcome_email.delay(created_user.id)  # type: ignore

        return UserResponse(
            id=created_user.id,
            email=created_user.email,
        )
