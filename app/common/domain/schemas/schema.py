__all__ = ("Schema",)

import typing as t

import pydantic

if t.TYPE_CHECKING:
    # NOTE: workaround for mypy not recognizing __class__
    # https://github.com/python/mypy/issues/4177
    # python reference:
    # https://docs.python.org/3/reference/datamodel.html#creating-the-class-object
    __class__: t.Type


from . import _exc
from . import _schema_registry


class Schema(pydantic.BaseModel):
    @classmethod
    def __pydantic_init_subclass__(cls, **kw: t.Any) -> None:
        super().__pydantic_init_subclass__(**kw)
        _schema_registry.add_schema(cls)

    def __new__(cls, *args: t.Any, **kw: t.Any) -> "Schema":
        if cls is __class__:
            raise _exc.SchemaNotInstantiableError(__class__)

        if not _schema_registry.has_rebuilt_schemas():
            raise _exc.SchemaNotRebuiltError(__class__, cls)

        return super().__new__(cls)

    @classmethod
    def rebuild_schemas(cls) -> None:
        _schema_registry.rebuild_schemas()
