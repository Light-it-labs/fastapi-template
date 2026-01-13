import typing as t

from pydantic import BaseModel
from pydantic import Field

_PageField = Field(ge=1)
_PageSizeField = Field(ge=1, le=100)


class PaginationSettings(BaseModel):
    page: t.Annotated[int, _PageField] = 1
    page_size: t.Annotated[int, _PageSizeField] = 10
    order: t.Literal["asc", "desc"] | None = None
    order_by: str | None = None


class PaginationInfo(BaseModel):
    page: t.Annotated[int, _PageField]
    page_size: t.Annotated[int, _PageSizeField]
    total: int
    total_pages: int


class PaginatedResponse[T](PaginationInfo):
    data: list[T]

    @classmethod
    def from_data(
        cls, data: list[T], info: PaginationInfo
    ) -> "PaginatedResponse[T]":
        return PaginatedResponse(data=data, **info.model_dump())
