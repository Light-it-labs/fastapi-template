from abc import ABC
from typing import Any, ClassVar

import pydantic

from app.templates import exceptions, types


class BaseTemplate(pydantic.BaseModel, ABC):
    __template_path__: ClassVar[str | None] = None
    __template_pipeline__: ClassVar[types.ProcessingPipeline | None] = None

    @classmethod
    def __init_subclass__(
        cls,
        path: str | None = None,
        pipeline: types.ProcessingPipeline | None = None,
        **kw: Any,
    ) -> None:
        super().__init_subclass__(**kw)

        if path:
            cls.__template_path__ = path

        if pipeline:
            cls.__template_pipeline__ = pipeline

    def get_path(self) -> str:
        if self.__template_path__:
            return self.__template_path__

        raise exceptions.TemplateMissingPathException(self)

    def get_pipeline(self) -> types.ProcessingPipeline:
        return self.__template_pipeline__ or tuple()

    def get_args(self) -> dict[str, Any]:
        return self.model_dump(exclude="path")
