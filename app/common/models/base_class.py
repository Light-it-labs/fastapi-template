from datetime import datetime
from enum import Enum
from typing import Literal
from uuid import UUID
from uuid import uuid4

from sqlalchemy import MetaData
from sqlalchemy import func
from sqlalchemy import types
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Base(DeclarativeBase):
    __abstract__ = True

    metadata = MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_%(constraint_name)s",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }
    )

    type_annotation_map = {
        UUID: types.UUID,
        datetime: types.DateTime(timezone=True),
        Enum: types.Enum(Enum, native_enum=False),
        Literal: types.Enum(Enum, native_enum=False),
    }

    id: Mapped[UUID] = mapped_column(
        default=uuid4,
        primary_key=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        server_onupdate=func.now(),
    )
