import uuid
from datetime import datetime

import sqlalchemy as sa
from sqlalchemy import orm


class BaseSQLAlchemyModel(orm.DeclarativeBase):
    __abstract__ = True

    metadata = sa.MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_%(constraint_name)s",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }
    )

    type_annotation_map = {
        uuid.UUID: sa.UUID,
        datetime: sa.DateTime(timezone=True),
    }

    id: orm.Mapped[uuid.UUID] = orm.mapped_column(
        default=uuid.uuid4,
        primary_key=True,
    )
    created_at: orm.Mapped[datetime] = orm.mapped_column(
        server_default=sa.func.now(),
    )
    updated_at: orm.Mapped[datetime] = orm.mapped_column(
        server_default=sa.func.now(),
        server_onupdate=sa.func.now(),
    )
