import fastapi

from app.common.exceptions import ModelNotCreatedException
from app.users.api.dependencies import CurrentUserDependency
from app.users.api.dependencies import UserRepositoryDependency
from app.users.domain import CreateUserRequest
from app.users.domain import UserResponse
from app.users.use_cases import CreateUserUseCase

router = fastapi.APIRouter()


@router.post("", status_code=fastapi.status.HTTP_201_CREATED)
def create_user(
    user_repository: UserRepositoryDependency,
    create_user_request: CreateUserRequest,
) -> UserResponse:
    try:
        return CreateUserUseCase(user_repository).execute(create_user_request)
    except ModelNotCreatedException:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_409_CONFLICT,
            detail="User with that email already registered.",
        )


@router.get("/current", status_code=fastapi.status.HTTP_200_OK)
def get_current_user(
    current_user: CurrentUserDependency,
) -> UserResponse:
    return UserResponse.model_validate(current_user)
