__all__ = ("BaseSQLAlchemyRepository",)

import abc
import typing as t
import uuid

import pydantic
import sqlalchemy as sa
import sqlalchemy.exc as sa_exc
from sqlalchemy import orm

from app.common.domain import Criteria
from app.common.domain import Entity
from app.common.domain import Repository
from app.common.exceptions import repository_errors

from .base_sqlalchemy_model import BaseSQLAlchemyModel


class BaseSQLAlchemyRepository[
    TEntity: Entity,
    TEntityId: uuid.UUID,
    TCreate: pydantic.BaseModel,
    TUpdate: pydantic.BaseModel,
    TModel: BaseSQLAlchemyModel,
](Repository[TEntity, TEntityId, TCreate, TUpdate], abc.ABC):
    @property
    @abc.abstractmethod
    def entity(self) -> type[TEntity]:
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def model(self) -> type[TModel]:
        raise NotImplementedError()

    def __init__(self, session: orm.Session):
        self._session = session

    # -------- Public interface --------
    # Single entity operations
    def find(self, entity_id: TEntityId) -> TEntity | None:
        model = self._get_by_id(entity_id)
        if model is None:
            return None

        return self._create_entity_from_model(model)

    def find_or_fail(self, entity_id: TEntityId) -> TEntity:
        entity = self.find(entity_id)
        if entity is None:
            self._raise_not_found()

        return entity

    def create(self, dto: TCreate) -> TEntity:
        stmt = (
            sa.insert(self.model)
            .values(**dto.model_dump())
            .returning(self.model)
        )

        try:
            model = self._session.execute(stmt).scalar_one()
        except (sa_exc.NoResultFound, sa_exc.IntegrityError):
            self._raise_not_created()

        return self._create_entity_from_model(model)

    def update(self, entity_id: TEntityId, dto: TUpdate) -> TEntity:
        stmt = (
            sa.update(self.model)
            .where(self.model.id == entity_id)
            .values(**dto.model_dump(exclude_unset=True))
            .returning(self.model)
        )

        try:
            model = self._session.execute(stmt).scalar_one()
        except (sa_exc.NoResultFound, sa_exc.MultipleResultsFound):
            self._raise_not_found()
        except sa_exc.IntegrityError:
            self._raise_not_updated()

        return self._create_entity_from_model(model)

    def delete(self, entity_id: TEntityId) -> None:
        stmt = (
            sa.delete(self.model)
            .where(self.model.id == entity_id)
            .returning(self.model.id)
        )

        try:
            self._session.execute(stmt).scalar_one()
        except (sa_exc.NoResultFound, sa_exc.MultipleResultsFound):
            self._raise_not_found()
        except sa_exc.IntegrityError:
            self._raise_not_deleted()

    # Multiple entity operations
    def all(self) -> list[TEntity]:
        stmt = sa.select(self.model)
        models = self._session.scalars(stmt)
        return self._create_entity_from_models(models)

    def where(self, *criteria: Criteria[TEntity]) -> list[TEntity]:
        raise NotImplementedError()

    def first(self, *criteria: Criteria[TEntity]) -> TEntity | None:
        raise NotImplementedError()

    def count(self, *criteria: Criteria[TEntity]) -> int:
        raise NotImplementedError()

    def exists(self, *criteria: Criteria[TEntity]) -> bool:
        raise NotImplementedError()

    # Bulk operations
    def insert_many(self, dtos: list[TCreate]) -> list[TEntity]:
        if not dtos:
            return []

        stmt = (
            sa.insert(self.model)
            .values([dto.model_dump() for dto in dtos])
            .returning(self.model)
        )

        models = self._session.scalars(stmt)
        entities = self._create_entity_from_models(models)

        if len(entities) != len(dtos):
            self._raise_not_created()

        return entities

    def update_where(self, dto: TUpdate, *criteria: Criteria[TEntity]) -> int:
        raise NotImplementedError()

    def delete_where(self, *criteria: Criteria[TEntity]) -> int:
        raise NotImplementedError()

    # ------- Private Helpers --------
    def _create_entity_from_model(self, model: TModel) -> TEntity:
        # TODO: rework with sentinel values to prevent eager loading on relationships
        try:
            return self.entity.model_validate(model)
        except pydantic.ValidationError as e:
            # TODO: raise a better message
            msg = f"Couldn't create entity instance.\n{e}"
            raise repository_errors.RepositoryError(msg)

    def _create_entity_from_models(
        self, models: t.Iterable[TModel]
    ) -> list[TEntity]:
        # TODO: rework to aggregate errors into an exception group?
        return [self._create_entity_from_model(model) for model in models]

    def _get_by_id(self, entity_id: TEntityId) -> TModel | None:
        return self._session.get(self.model, entity_id)

    def _raise_not_found(self) -> t.NoReturn:
        """Override if a better message is required"""
        raise repository_errors.EntityNotFoundError(self.entity)

    def _raise_not_created(self) -> t.NoReturn:
        """Override if a better message is required"""
        raise repository_errors.EntityNotCreatedError(self.entity)

    def _raise_not_updated(self) -> t.NoReturn:
        """Override if a better message is required"""
        raise repository_errors.EntityNotUpdatedError(self.entity)

    def _raise_not_deleted(self) -> t.NoReturn:
        """Override if a better message is required"""
        raise repository_errors.EntityNotDeletedError(self.entity)
