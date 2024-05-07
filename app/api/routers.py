from fastapi import APIRouter

from app.api.v1.endpoints import auth, users, health_checks

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(
    health_checks.router, prefix="/health", tags=["health"]
)
