from typing import Annotated, Literal

from pydantic import BaseModel
from pydantic import Field

_PageField = Field(ge=1)
_PageSizeField = Field(ge=1, le=100)


class PaginationSettings(BaseModel):
    page: Annotated[int, _PageField] = 1
    page_size: Annotated[int, _PageSizeField] = 10
    order: Literal["asc", "desc"] | None = None
    order_by: str | None = None


class PaginationInfo(BaseModel):
    page: Annotated[int, _PageField]
    page_size: Annotated[int, _PageSizeField]
    total: int
    total_pages: int


class PaginatedResponse[T](PaginationInfo):
    data: list[T]
