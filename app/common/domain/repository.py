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
        """Return entity by ID or None if not found."""

    @abc.abstractmethod
    def find_or_fail(self, entity_id: TEntityId) -> TEntity:
        """Return entity by ID or raise EntityNotFoundError."""

    @abc.abstractmethod
    def create(self, dto: TCreate) -> TEntity:
        """Persist a new entity and return it."""

    @abc.abstractmethod
    def update(self, entity_id: TEntityId, dto: TUpdate) -> TEntity:
        """Update an existing entity and return it."""

    @abc.abstractmethod
    def delete(self, entity_id: TEntityId) -> None:
        """Delete an entity by ID."""

    # Multiple entity operations
    @abc.abstractmethod
    def all(self) -> list[TEntity]:
        """Return all entities."""

    @abc.abstractmethod
    def where(self, *criteria: Criteria[TEntity]) -> list[TEntity]:
        """Return entities matching all given criteria."""

    @abc.abstractmethod
    def first(self, *criteria: Criteria[TEntity]) -> TEntity | None:
        """Return first entity matching criteria or None."""

    @abc.abstractmethod
    def count(self, *criteria: Criteria[TEntity]) -> int:
        """Return count of entities matching criteria."""

    @abc.abstractmethod
    def exists(self, *criteria: Criteria[TEntity]) -> bool:
        """Return True if any entity matches criteria."""

    # Bulk operations
    @abc.abstractmethod
    def insert_many(self, dtos: list[TCreate]) -> list[TEntity]:
        """Persist multiple new entities and return them."""

    @abc.abstractmethod
    def update_where(self, dto: TUpdate, *criteria: Criteria[TEntity]) -> int:
        """Update entities matching criteria and return count of updated rows."""

    @abc.abstractmethod
    def delete_where(self, *criteria: Criteria[TEntity]) -> int:
        """Delete entities matching criteria and return count of deleted rows."""
