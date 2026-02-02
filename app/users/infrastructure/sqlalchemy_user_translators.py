__all__ = ("SQLAlchemyUserEmailFilterTranslator",)

from app.common.infrastructure import SqlalchemyCriteriaTranslator
from app.common.infrastructure import Statement
from app.users.domain import UserEmailFilter

from .sqlalchemy_user_model import SQLAlchemyUserModel


class SQLAlchemyUserEmailFilterTranslator(
    SqlalchemyCriteriaTranslator[UserEmailFilter],
    criteria=UserEmailFilter,
):
    def translate(self, stmt: Statement) -> Statement:
        return stmt.where(SQLAlchemyUserModel.email == self._criteria.email)
