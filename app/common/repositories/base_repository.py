from math import ceil
from typing import Any, Generic, List, Type, TypeVar
from uuid import UUID

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import asc, desc
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.orm.query import Query

from app.common.schemas.pagination_schema import ListFilter, ListResponse


ModelType = TypeVar("ModelType", bound=Any)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(
        self, model: Type[ModelType], joined_loads: List[str] | None = None
    ):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model
        self.joined_loads = joined_loads

    def get(
        self,
        db: Session,
        model_id: UUID,
    ) -> ModelType | None:
        query = db.query(self.model).filter(self.model.id == model_id)

        if self.joined_loads is not None:
            for relation in self.joined_loads:
                query = query.options(
                    joinedload(getattr(self.model, relation))
                )

        return query.first()

    def list(
        self, db: Session, list_options: ListFilter, query: Query | None = None
    ) -> ListResponse:
        if not query:
            query = db.query(self.model)

        total = query.count()

        if list_options.order_by:
            column = list_options.order_by
            direction = list_options.order
            by = desc if direction == "desc" else asc

            query = query.order_by(by(column))

        query = query.offset(list_options.page_size * (list_options.page - 1))

        query = query.limit(list_options.page_size)
        return ListResponse(
            data=query.all(),
            page=list_options.page,
            page_size=list_options.page_size,
            total=total,
            total_pages=ceil(total / list_options.page_size),
        )

    def create(self, db: Session, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.flush()
        return db_obj

    def update(
        self, db: Session, db_obj: ModelType, obj_in: UpdateSchemaType
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.model_dump(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.flush()
        return db_obj

    def delete(self, db: Session, model_id: UUID) -> ModelType | None:
        obj = db.query(self.model).get(model_id)
        db.delete(obj)
        db.flush()
        return obj
