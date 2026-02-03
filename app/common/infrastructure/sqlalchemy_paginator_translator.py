from app.common.domain import PaginationCriteria

from .sqlalchemy_criteria_translator import SqlalchemyCriteriaTranslator
from .sqlalchemy_criteria_translator import Statement


class SQLAlchemyPaginationTranslator(
    SqlalchemyCriteriaTranslator[PaginationCriteria],
    criteria=PaginationCriteria,
):
    def translate(self, stmt: Statement) -> Statement:
        page_size = self._criteria.page_size
        page = self._criteria.page
        offset = (page - 1) * page_size

        return stmt.offset(offset).limit(page_size)
