__all__ = ("UserRepository",)

from app.common.domain import Repository

from .user import User
from .user_types import UserId


class UserRepository(
    Repository[
        User,
        UserId,
        User.CreateDto,
        User.UpdateDto,
    ]
):
    pass
