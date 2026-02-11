__all__ = ("Schema",)

import threading
import typing as t

import pydantic

if t.TYPE_CHECKING:
    # NOTE: workaround for mypy not recognizing __class__
    # https://github.com/python/mypy/issues/4177
    # python reference:
    # https://docs.python.org/3/reference/datamodel.html#creating-the-class-object
    __class__: t.Type


type _SchemaRegistry = list[type["Schema"]]

_Mutex: t.Final = threading.Lock()


class Schema(pydantic.BaseModel):
    _rebuilt_models: t.ClassVar[bool] = False
    _registry: t.ClassVar[_SchemaRegistry] = []

    @classmethod
    def __pydantic_init_subclass__(cls, **kw: t.Any) -> None:
        super().__pydantic_init_subclass__(**kw)
        __class__._registry.append(cls)

    def __new__(cls, *args: t.Any, **kw: t.Any) -> "Schema":
        if cls is __class__:
            raise SchemaNotInstantiableError()

        if not cls._rebuilt_models:
            raise SchemaNotRebuiltError(cls)

        return super().__new__(cls)

    @classmethod
    def rebuild_models(cls) -> None:
        with _Mutex:
            cls._rebuild_models()

    @classmethod
    def _rebuild_models(cls) -> None:
        if cls._rebuilt_models:
            return

        errors = _rebuild_and_collect_errors(cls._registry)

        if errors:
            msg = "Failed to build schemas"
            raise ExceptionGroup(msg, errors)

        cls._rebuilt_models = True


def _rebuild_and_collect_errors(
    registry: _SchemaRegistry,
) -> list[Exception]:
    results = (_rebuild_schema(schema) for schema in registry)
    errors = (result for result in results if result is not None)

    return list(errors)


def _rebuild_schema(schema: type[Schema]) -> Exception | None:
    result: Exception | None
    try:
        schema.model_rebuild()
    except Exception as error:
        result = error
    else:
        result = None

    return result


class SchemaNotInstantiableError(Exception):
    def __init__(self) -> None:
        msg = (
            f"Class `{Schema.__name__}` is a base class. "
            "It should not be instantiated"
        )
        super().__init__(msg)


class SchemaNotRebuiltError(Exception):
    def __init__(self, schema: type[Schema]) -> None:
        msg = (
            f"Schema not rebuilt: {schema.__name__}\n"
            f"Must call `{Schema.__name__}.rebuild_models()` before instantiating schemas"
        )
        super().__init__(msg)
