from sqlalchemy.orm import Session


from app.common.repositories.base_repository import BaseRepository
from app.users.models.user import User
from app.users.schemas.user_schema import UserCreate, UserUpdate


class UsersRepository(BaseRepository[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, email: str) -> User | None:
        return db.query(self.model).filter(User.email == email).first()


users_repository = UsersRepository(User)
