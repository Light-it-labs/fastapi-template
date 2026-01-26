__all__ = ("Repository",)

import abc
import uuid

import pydantic

from .criteria import Criteria
from .entities import Entity


class Repository[
    TEntity: Entity,
    TEntityId: uuid.UUID,
    TCreate: pydantic.BaseModel,
    TUpdate: pydantic.BaseModel,
](abc.ABC):
    # Single entity operations
    @abc.abstractmethod
    def find(self, entity_id: TEntityId) -> TEntity | None:
        raise NotImplementedError()

    @abc.abstractmethod
    def find_or_fail(self, entity_id: TEntityId) -> TEntity:
        raise NotImplementedError()

    @abc.abstractmethod
    def create(self, dto: TCreate) -> TEntity:
        raise NotImplementedError()

    @abc.abstractmethod
    def update(self, entity_id: TEntityId, dto: TUpdate) -> TEntity:
        raise NotImplementedError()

    @abc.abstractmethod
    def delete(self, entity_id: TEntityId) -> None:
        raise NotImplementedError()

    # Multiple entity operations
    @abc.abstractmethod
    def all(self) -> list[TEntity]:
        raise NotImplementedError()

    @abc.abstractmethod
    def where(self, *criteria: Criteria[TEntity]) -> list[TEntity]:
        raise NotImplementedError()

    @abc.abstractmethod
    def first(self, *criteria: Criteria[TEntity]) -> TEntity | None:
        raise NotImplementedError()

    @abc.abstractmethod
    def count(self, *criteria: Criteria[TEntity]) -> int:
        raise NotImplementedError()

    @abc.abstractmethod
    def exists(self, *criteria: Criteria[TEntity]) -> bool:
        raise NotImplementedError()

    # Bulk operations
    @abc.abstractmethod
    def insert_many(self, dtos: list[TCreate]) -> list[TEntity]:
        raise NotImplementedError()

    @abc.abstractmethod
    def update_where(self, dto: TUpdate, *criteria: Criteria[TEntity]) -> int:
        raise NotImplementedError()

    @abc.abstractmethod
    def delete_where(self, *criteria: Criteria[TEntity]) -> int:
        raise NotImplementedError()
