from typing import Literal, Annotated

from pydantic import BaseModel, Field

_PageField = Field(ge=1)
_PageSizeField = Field(ge=1, le=100)


class ListFilter(BaseModel):
    page: Annotated[int, _PageField] = 1
    page_size: Annotated[int, _PageSizeField] = 10
    order: Literal["asc", "desc"] | None = None
    order_by: str | None = None


class ListResponse[T](BaseModel):
    data: list[T]
    page: Annotated[int, _PageField]
    page_size: Annotated[int, _PageSizeField]
    total: int
    total_pages: int
