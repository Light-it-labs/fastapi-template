from fastapi import APIRouter

from app.users.api import endpoints

api_router = APIRouter()
api_router.include_router(endpoints.router, prefix="/users", tags=["users"])
