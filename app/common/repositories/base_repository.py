from math import ceil
from typing import Any, Generic, Optional, Type, TypeVar
from uuid import UUID

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import asc, desc
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.query import Query

from app.common.schemas.pagination_schema import ListFilter, ListResponse


ModelType = TypeVar("ModelType", bound=Any)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    async def get(
        self, session: AsyncSession, model_id: UUID
    ) -> Optional[ModelType]:
        result = await session.execute(
            select(self.model).filter(self.model.id == model_id)
        )
        return result.scalars().first()

    async def list(
        self,
        session: AsyncSession,
        list_options: ListFilter,
        query: Query | None = None,
    ) -> ListResponse:
        if not query:
            query = await session.execute(select(self.model))

        total = query.count()

        if list_options.order_by:
            column = list_options.order_by
            direction = list_options.order
            by = desc if direction == "desc" else asc

            query = query.order_by(by(column))

        query = query.offset(list_options.page_size * (list_options.page - 1))

        query = query.limit(list_options.page_size)
        return ListResponse(
            data=await query.all(),
            page=list_options.page,
            page_size=list_options.page_size,
            total=total,
            total_pages=ceil(total / list_options.page_size),
        )

    async def create(
        self, session: AsyncSession, obj_in: CreateSchemaType
    ) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def update(
        self,
        session: AsyncSession,
        db_obj: ModelType,
        obj_in: UpdateSchemaType,
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def delete(
        self, session: AsyncSession, model_id: UUID
    ) -> ModelType | None:
        obj = await self.get(session, model_id)
        await session.delete(obj)
        await session.commit()
        return obj
