import abc
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

type _Statement[TModel: Base] = sa.Select[tuple[TModel]]


class BaseQueryProcessor[TModel: Base](abc.ABC):
    @abc.abstractmethod
    def __call__(self, stmt: _Statement[TModel]) -> _Statement[TModel]:
        pass


class Paginator[TModel: Base](BaseQueryProcessor):
    _session: Session
    _settings: PaginationSettings
    _info: PaginationInfo | None

    @property
    def info(self) -> PaginationInfo:
        if self._info is None:
            self._raise_invalid_state()

        return self._info

    def __init__(self, db: Session, settings: PaginationSettings) -> None:
        self._session = db
        self._settings = settings
        self._info = None

    def __call__(self, stmt: _Statement[TModel]) -> _Statement[TModel]:
        if self._info is not None:
            self._raise_invalid_state()

        total = self._get_total(stmt)

        stmt = self._order(stmt)

        page = self._settings.page
        page_size = self._settings.page_size
        offset = page_size * (page - 1)

        stmt = stmt.offset(offset)
        stmt = stmt.limit(page_size)

        total_pages = ceil(total / page_size)
        if page > total_pages:
            page = total_pages

        self._info = PaginationInfo(
            page=page,
            page_size=page_size,
            total=total,
            total_pages=total_pages,
        )

        return stmt

    def _get_total(self, stmt: _Statement[TModel]) -> int:
        total_stmt = sa.select(sa.func.count("*")).select_from(stmt.subquery())
        return self._session.execute(total_stmt).scalar_one()

    def _order(self, stmt: _Statement[TModel]) -> _Statement[TModel]:
        if self._settings.order_by is None:
            return stmt

        column = self._settings.order_by
        direction = self._settings.order
        by = sa.desc if direction == "desc" else sa.asc

        return stmt.order_by(by(column))

    def _raise_invalid_state(self) -> t.NoReturn:
        mod = "already" if self._info is not None else "not"
        msg = f"Paginator has {mod} run"
        raise RuntimeError(msg)


class BaseRepository[
    TModel: Base,
    TCreate: BaseModel,
    TUpdate: BaseModel,
]:
    model: type[TModel]

    def __init_subclass__(cls, *, model: type[TModel]) -> None:
        cls.model = model

    def get_by_id(self, db: Session, model_id: UUID) -> TModel | None:
        stmt = sa.select(self.model).where(self.model.id == model_id)

        return db.execute(stmt).scalar_one_or_none()

    def list_all(
        self, db: Session, processor: BaseQueryProcessor | None = None
    ) -> list[TModel]:
        stmt = sa.select(self.model)
        if processor is not None:
            stmt = processor(stmt)

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
