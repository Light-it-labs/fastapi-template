from typing import Annotated, AsyncGenerator

from app.db.database_session_manager import DatabaseSessionManager
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession


async def get_session() -> AsyncGenerator:
    session_manager = DatabaseSessionManager().init()
    async with session_manager.session() as session:
        yield session


SessionDependency = Annotated[AsyncSession, Depends(get_session)]
