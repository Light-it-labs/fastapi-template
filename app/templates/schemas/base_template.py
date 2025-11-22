from abc import ABC, abstractmethod
from typing import Any, ClassVar

import pydantic

import app.templates.types as _types


class BaseTemplate(pydantic.BaseModel, ABC):
    @property
    @abstractmethod
    def path(self) -> str:
        pass

    pipeline: ClassVar[_types.PostProcessingPipeline] = tuple()

    def get_args(self) -> dict[str, Any]:
        return self.model_dump(exclude="path")
