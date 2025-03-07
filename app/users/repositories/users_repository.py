from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession


from app.common.repositories.base_repository import BaseRepository
from app.users.models.user import User
from app.users.schemas.user_schema import UserCreate, UserUpdate


class UsersRepository(BaseRepository[User, UserCreate, UserUpdate]):
    async def get_by_email(
        self, session: AsyncSession, email: str
    ) -> User | None:
        result = await session.execute(
            select(self.model).filter(User.email == email)
        )
        return result.scalars().first()


users_repository = UsersRepository(User)
