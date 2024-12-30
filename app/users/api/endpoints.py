from fastapi import APIRouter, status

from app.users.schemas.user_schema import CreateUserRequest, UserResponse
from app.users.use_cases.create_user_use_case import CreateUserUseCase
from app.users.api.dependencies.get_current_user import CurrentUser
from app.common.api.dependencies.get_db import SessionDependency

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
