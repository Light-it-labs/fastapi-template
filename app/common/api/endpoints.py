from fastapi import APIRouter, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from starlette import status

from app.db.session import engine

router = APIRouter()


@router.get("")
def check_database_health() -> dict:
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return {"status": "ok", "message": "Database is healthy"}
    except OperationalError as e:
        error_message = str(e)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database is " f"unhealthy: {error_message}",
        )
