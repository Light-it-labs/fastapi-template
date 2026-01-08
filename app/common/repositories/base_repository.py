from math import ceil
from uuid import UUID

import sqlalchemy as sa
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.common.exceptions import ModelNotFoundException
from app.common.models import Base
from app.common.schemas.pagination_schema import ListFilter
from app.common.schemas.pagination_schema import ListResponse


class BaseRepository[TModel: Base, TCreate: BaseModel, TUpdate: BaseModel]:
    MODEL_CLS: type[TModel]

    def __init_subclass__(cls, *, model_cls: type[TModel]) -> None:
        cls.MODEL_CLS = model_cls

    def get_by_id(self, db: Session, model_id: UUID) -> TModel | None:
        stmt = sa.select(self.MODEL_CLS).where(self.MODEL_CLS.id == model_id)

        return db.execute(stmt).scalar_one_or_none()

    def list(
        self,
        db: Session,
        list_options: ListFilter,
        stmt: sa.Select[tuple[TModel]] | None = None,
    ) -> ListResponse:
        if stmt is None:
            stmt = sa.select(self.MODEL_CLS)

        total_stmt = sa.select(sa.func.count("*")).select_from(stmt.subquery())
        total = db.execute(total_stmt).scalar_one()

        if list_options.order_by:
            column = list_options.order_by
            direction = list_options.order
            by = sa.desc if direction == "desc" else sa.asc

            stmt = stmt.order_by(by(column))

        stmt = stmt.offset(list_options.page_size * (list_options.page - 1))
        stmt = stmt.limit(list_options.page_size)

        data = list(db.scalars(stmt))

        return ListResponse(
            data=data,
            page=list_options.page,
            page_size=list_options.page_size,
            total=total,
            total_pages=ceil(total / list_options.page_size),
        )

    def create(self, db: Session, schema: TCreate) -> TModel:
        model = self.MODEL_CLS(**schema.model_dump())
        db.add(model)
        db.flush()
        return model

    def update(self, db: Session, model_id: UUID, data: TUpdate) -> TModel:
        stmt = (
            sa.update(self.MODEL_CLS)
            .where(self.MODEL_CLS.id == model_id)
            .values(data.model_dump(exclude_unset=True))
            .returning(self.MODEL_CLS)
        )

        model = db.execute(stmt).scalar_one_or_none()

        if model is None:
            raise ModelNotFoundException()

        return model

    def delete(self, db: Session, model_id: UUID) -> TModel | None:
        stmt = (
            sa.delete(self.MODEL_CLS)
            .where(self.MODEL_CLS.id == model_id)
            .returning(self.MODEL_CLS)
        )

        return db.execute(stmt).scalar_one_or_none()
