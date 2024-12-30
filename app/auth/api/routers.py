from fastapi import APIRouter

from app.api.v1.endpoints import users
from app.auth.api import endpoints

api_router = APIRouter()
api_router.include_router(endpoints.router, prefix="/auth", tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
