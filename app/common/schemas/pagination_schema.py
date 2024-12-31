from typing import Generic, List, Literal, TypeVar

from pydantic import BaseModel, conint


class ListFilter(BaseModel):
    page: conint(ge=1) = 1
    page_size: conint(ge=1, le=100) = 10
    name: str | None = None
    order: Literal["asc", "desc"] | None = None
    order_by: str | None = None


T = TypeVar("T")


class ListResponse(BaseModel, Generic[T]):
    data: List[T]
    page_size: conint(ge=1, le=100)
    page: conint(ge=1)
    total: int
    total_pages: int
