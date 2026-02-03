__all__ = ("SQLAlchemyUserEmailFilterTranslator",)

from app.common.infrastructure import SqlalchemyCriteriaTranslator
from app.common.infrastructure import Statement
from app.users.domain import UserEmailFilterCriteria

from .sqlalchemy_user_model import SQLAlchemyUserModel


class SQLAlchemyUserEmailFilterTranslator(
    SqlalchemyCriteriaTranslator[UserEmailFilterCriteria],
    criteria=UserEmailFilterCriteria,
):
    def translate(self, stmt: Statement) -> Statement:
        return stmt.where(SQLAlchemyUserModel.email == self._criteria.email)
