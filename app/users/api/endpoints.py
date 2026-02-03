import fastapi

import app.users.domain as user_domain
import app.users.errors as user_errors
import app.users.use_cases as use_cases
from app.users.api.dependencies import CurrentUserDependency
from app.users.api.dependencies import UserRepositoryDependency

router = fastapi.APIRouter()


@router.post("", status_code=fastapi.status.HTTP_201_CREATED)
def create_user(
    user_repository: UserRepositoryDependency,
    create_user_request: user_domain.CreateUserRequest,
) -> user_domain.UserResponse:
    use_case = use_cases.CreateUserUseCase(user_repository)

    try:
        return use_case.execute(create_user_request)
    except user_errors.UserEmailCollisionError as e:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_409_CONFLICT,
            detail=e.message,
        )


@router.get("/current", status_code=fastapi.status.HTTP_200_OK)
def get_current_user(
    current_user: CurrentUserDependency,
) -> user_domain.UserResponse:
    return user_domain.UserResponse.model_validate(current_user)
