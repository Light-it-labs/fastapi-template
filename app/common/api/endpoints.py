from app.db.database_session_manager import DatabaseSessionManager
from fastapi import APIRouter, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from starlette import status

router = APIRouter()


@router.get("")
async def check_database_health() -> dict:
    session_manager = DatabaseSessionManager().init()
    try:
        async with session_manager.session() as session:
            session.execute(text("SELECT 1"))
        return {"status": "ok", "message": "Database is healthy"}
    except OperationalError as e:
        error_message = str(e)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database is unhealthy: {error_message}",
        )
