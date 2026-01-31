__all__ = ("CreateUserUseCase",)

from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

import app.users.domain as user_domain
from app.auth.utils import security
from app.users.infrastructure import SQLAlchemyUserRepository


class CreateUserUseCase:
    # TODO: abstract with dependencies
    def __init__(self, session: Session):
        self.repository = SQLAlchemyUserRepository(session)

    def execute(
        self,
        create_user_request: user_domain.CreateUserRequest,
    ) -> user_domain.UserResponse:
        # from app.celery.tasks.emails import send_welcome_email

        if self.repository.exists(
            user_domain.UserEmailFilter(create_user_request.email),
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with that email already registered.",
            )

        created_user = self.repository.create(
            user_domain.User.CreateDto(
                email=create_user_request.email,
                hashed_password=security.get_password_hash(
                    create_user_request.password
                ),
            )
        )

        # send_welcome_email.delay(created_user.id)  # type: ignore

        return user_domain.UserResponse(
            id=created_user.id,
            email=created_user.email,
        )
