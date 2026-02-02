__all__ = ("Paginator",)

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


class Paginator(pydantic.BaseModel, Criteria[t.Any]):
    page: _PageField = 1
    page_size: _PageSizeField = 10
