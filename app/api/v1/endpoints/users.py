from fastapi import APIRouter, status

from app.api.dependencies.get_current_user import CurrentUser
from app.schemas.user_schema import UserResponse

router = APIRouter()


@router.get("/current", status_code=status.HTTP_200_OK)
def get_current_patient(
    current_user: CurrentUser,
) -> UserResponse:
    return UserResponse.model_validate(current_user)
