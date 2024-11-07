from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from fastapi import status

from app.api.dependencies.get_current_user import UsersService
from app.repositories.users_repository import UserCreate, users_repository
from app.schemas.user_schema import CreateUserRequest, UserResponse


class CreateUserUseCase:
    def __init__(self, session: Session):
        self.session = session

    def execute(self, create_user_request: CreateUserRequest) -> UserResponse:
        users_service = UsersService(self.session, users_repository)
        if users_service.get_by_email(create_user_request.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with that email already registered.",
            )

        created_user = UsersService(
            self.session, users_repository
        ).create_user(
            UserCreate(
                email=create_user_request.email,
                hashed_password=create_user_request.password,
            )
        )
        return UserResponse(
            id=created_user.id,
            email=created_user.email,
        )
