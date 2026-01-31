__all__ = ("SQLAlchemyUserRepository",)

from app.common.infrastructure import BaseSQLAlchemyRepository
from app.users.domain import User
from app.users.domain import UserRepository
from app.users.domain.user_types import UserId

from .sqlalchemy_user_model import SQLAlchemyUserModel


class SQLAlchemyUserRepository(
    BaseSQLAlchemyRepository[
        User,
        UserId,
        User.CreateDto,
        User.UpdateDto,
        SQLAlchemyUserModel,
    ],
    UserRepository,
):
    entity = User
    model = SQLAlchemyUserModel
