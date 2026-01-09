import typing as t
from math import ceil
from uuid import UUID

import sqlalchemy as sa
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.common.exceptions import ModelNotFoundException
from app.common.models import Base
from app.common.schemas.pagination_schema import PaginationInfo
from app.common.schemas.pagination_schema import PaginationSettings


class _PaginatorOutput[TModel: Base](t.NamedTuple):
    stmt: sa.Select[tuple[TModel]]
    info: PaginationInfo


class Paginator:
    def __init__(self, settings: PaginationSettings) -> None:
        self._settings = settings

    def __call__[TModel: Base](
        self,
        db: Session,
        stmt: sa.Select[tuple[TModel]],
    ) -> _PaginatorOutput[TModel]:
        total_stmt = sa.select(sa.func.count("*")).select_from(stmt.subquery())

        total = db.execute(total_stmt).scalar_one()

        if self._settings.order_by is not None:
            column = self._settings.order_by
            direction = self._settings.order
            by = sa.desc if direction == "desc" else sa.asc
            stmt = stmt.order_by(by(column))

        page = self._settings.page
        page_size = self._settings.page_size
        offset = page_size * (page - 1)

        stmt = stmt.offset(offset)
        stmt = stmt.limit(page_size)

        total_pages = ceil(total / page_size)
        if page > total_pages:
            page = total_pages

        return _PaginatorOutput(
            stmt,
            PaginationInfo(
                page=page,
                page_size=page_size,
                total=total,
                total_pages=total_pages,
            ),
        )


class BaseRepository[
    TModel: Base,
    TCreate: BaseModel,
    TUpdate: BaseModel,
]:
    _DEFAULT_MODEL: type[TModel]

    def __init_subclass__(cls, *, model: type[TModel]) -> None:
        cls._DEFAULT_MODEL = model

    def __init__(self, model: type[TModel] | None = None) -> None:
        self.model = self._DEFAULT_MODEL if model is None else model

    def get_by_id(self, db: Session, model_id: UUID) -> TModel | None:
        stmt = sa.select(self.model).where(self.model.id == model_id)

        return db.execute(stmt).scalar_one_or_none()

    def list_paginated(
        self, db: Session, paginator: Paginator
    ) -> tuple[list[TModel], PaginationInfo]:
        stmt = sa.select(self.model)

        stmt, pagination_info = paginator(db, stmt)
        data = list(db.scalars(stmt))

        return data, pagination_info

    def list_all(self, db: Session) -> list[TModel]:
        stmt = sa.select(self.model)

        return list(db.scalars(stmt))

    def create(self, db: Session, schema: TCreate) -> TModel:
        model = self.model(**schema.model_dump())
        db.add(model)
        db.flush()
        return model

    def update(self, db: Session, model_id: UUID, data: TUpdate) -> TModel:
        stmt = (
            sa.update(self.model)
            .where(self.model.id == model_id)
            .values(data.model_dump(exclude_unset=True))
            .returning(self.model)
        )

        model = db.execute(stmt).scalar_one_or_none()

        if model is None:
            raise ModelNotFoundException()

        return model

    def delete(self, db: Session, model_id: UUID) -> TModel | None:
        stmt = (
            sa.delete(self.model)
            .where(self.model.id == model_id)
            .returning(self.model)
        )

        return db.execute(stmt).scalar_one_or_none()
