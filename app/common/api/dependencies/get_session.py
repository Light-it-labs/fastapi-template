__all__ = (
    "get_session",
    "SessionDependency",
)

import typing as t

import fastapi
from sqlalchemy.orm import Session

from app.db.session import SessionLocal


def get_session() -> t.Generator[Session, None, None]:
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


SessionDependency = t.Annotated[
    Session,
    fastapi.Depends(get_session),
]
