from typing import Annotated, Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import SessionLocal


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


SessionDependency = Annotated[Session, Depends(get_db)]
