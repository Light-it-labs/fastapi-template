from fastapi import APIRouter

from app.users.api import providers

api_router = APIRouter()
api_router.include_router(
    providers.router, prefix="/providers", tags=["providers"]
)
