from fastapi import APIRouter, status

from app.api.dependencies.get_current_user import (
    CurrentUser,
    SessionDependency,
)
from app.schemas.user_schema import CreateUserRequest, UserResponse
from app.use_cases.users.create_user_use_case import CreateUserUseCase

router = APIRouter()


@router.get("/current", status_code=status.HTTP_200_OK)
def get_current_user(
    current_user: CurrentUser,
) -> UserResponse:
    return UserResponse.model_validate(current_user)


@router.post("", status_code=status.HTTP_201_CREATED)
def create_user(
    session: SessionDependency,
    create_user_request: CreateUserRequest,
) -> UserResponse:
    return CreateUserUseCase(session).execute(create_user_request)
