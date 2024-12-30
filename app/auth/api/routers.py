from fastapi import APIRouter

from app.auth.api import endpoints

api_router = APIRouter()
api_router.include_router(endpoints.router, prefix="/auth", tags=["login"])
