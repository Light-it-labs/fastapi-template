from typing import Optional

from sqlalchemy.orm import Session

from app.models import User
from app.repositories.base_repository import BaseRepository
from app.schemas.user_schema import UserCreate, UserUpdate


class UsersRepository(BaseRepository[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()


users_repository = UsersRepository(User)
