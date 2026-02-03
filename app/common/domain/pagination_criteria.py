__all__ = ("PaginationCriteria",)

import typing as t

import pydantic

from .criteria import Criteria

_PageField = t.Annotated[
    int,
    pydantic.Field(ge=1),
]
_PageSizeField = t.Annotated[
    int,
    pydantic.Field(ge=1, le=100),
]


class PaginationCriteria(pydantic.BaseModel, Criteria[t.Any]):
    model_config = pydantic.ConfigDict(frozen=True)

    page: _PageField = 1
    page_size: _PageSizeField = 10
