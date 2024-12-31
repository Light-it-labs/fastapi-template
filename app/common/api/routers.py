from fastapi import APIRouter

from app.common.api import endpoints

api_router = APIRouter()
api_router.include_router(endpoints.router, prefix="/health", tags=["health"])
