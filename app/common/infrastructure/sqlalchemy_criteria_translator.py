__all__ = ("SqlalchemyCriteriaTranslator",)

import abc
import typing as t

import sqlalchemy as sa

from app.common.domain import Criteria

type _Statement = sa.Select[t.Any] | sa.Update | sa.Delete
type _Criteria = Criteria[t.Any]
type _Translator = "SqlalchemyCriteriaTranslator[t.Any]"
type _Registry = dict[type[_Criteria], type[_Translator]]


class SqlalchemyCriteriaTranslator[TCriteria: _Criteria](abc.ABC):
    _registry: t.ClassVar[_Registry] = {}

    def __init_subclass__(
        cls,
        *,
        criteria: type[_Criteria] | None = None,
        **kw: t.Any,
    ) -> None:
        super().__init_subclass__(**kw)
        if criteria is not None:
            cls._registry[criteria] = cls

    def __init__(self, criteria: TCriteria) -> None:
        self._criteria = criteria

    @classmethod
    def get_for_criteria(cls, criteria: _Criteria) -> _Translator:
        translator_cls = cls._registry.get(type(criteria), None)
        if translator_cls is None:
            raise NoTranslatorForCriteriaError(criteria)

        return translator_cls(criteria)

    @abc.abstractmethod
    def translate(self, stmt: _Statement) -> _Statement:
        raise NotImplementedError()


class SqlalchemyCriteriaTranslatorError(Exception):
    pass


class NoTranslatorForCriteriaError(SqlalchemyCriteriaTranslatorError):
    def __init__(self, criteria: _Criteria):
        criteria_name = type(criteria).__name__
        msg = f"No translator for {criteria_name}"
        super().__init__(msg)
