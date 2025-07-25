from fastapi import APIRouter

from app.two_factor_authentication.api import endpoints

api_router = APIRouter()
api_router.include_router(
    endpoints.router, prefix="/users/{user_id}/totp", tags=["totp"]
)
