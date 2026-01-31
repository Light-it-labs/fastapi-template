__all__ = (
    "UserEmailFilter",
    "UserCriteria",
)

import dataclasses

from app.common.domain import Criteria

from .user import User


class UserCriteria(Criteria[User]):
    pass


@dataclasses.dataclass(frozen=True)
class UserEmailFilter(UserCriteria):
    email: str
