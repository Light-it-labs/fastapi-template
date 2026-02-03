__all__ = ("CreateUserUseCase",)

import app.users.domain as user_domain
from app.auth.utils import security
from app.users.errors import UserEmailCollisionError


class CreateUserUseCase:
    def __init__(self, user_repository: user_domain.UserRepository):
        self.user_repository = user_repository

    def execute(
        self,
        create_user_request: user_domain.CreateUserRequest,
    ) -> user_domain.UserResponse:
        from app.celery.tasks.emails import send_welcome_email

        if self.user_repository.exists(
            user_domain.UserEmailFilterCriteria(create_user_request.email),
        ):
            raise UserEmailCollisionError(create_user_request.email)

        created_user = self.user_repository.create(
            user_domain.User.CreateDto(
                email=create_user_request.email,
                hashed_password=security.get_password_hash(
                    create_user_request.password
                ),
            )
        )

        send_welcome_email.delay(created_user.id)

        return user_domain.UserResponse(
            id=created_user.id,
            email=created_user.email,
        )
