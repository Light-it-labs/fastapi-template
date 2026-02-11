__all__ = (
    "add_schema",
    "has_rebuilt_schemas",
    "rebuild_schemas",
)

import threading
import typing as t

import pydantic

# region types
_Schema = type[pydantic.BaseModel]
_Registry = list[_Schema]


# region public api
def add_schema(schema: _Schema) -> None:
    _registry.append(schema)


def rebuild_schemas() -> None:
    with _rebuilding_mutex:
        _rebuild_schemas()


def has_rebuilt_schemas() -> bool:
    return _has_rebuilt_schemas


# region private
_registry: _Registry = []
_has_rebuilt_schemas: bool = False
_rebuilding_mutex: t.Final = threading.Lock()


def _rebuild_schemas() -> None:
    global _has_rebuilt_schemas

    if _has_rebuilt_schemas:
        return

    errors = _rebuild_and_collect_errors()

    if errors:
        msg = "Failed to build schemas"
        raise ExceptionGroup(msg, errors)

    _has_rebuilt_schemas = True


def _rebuild_and_collect_errors() -> list[Exception]:
    results = (_rebuild_schema(schema) for schema in _registry)
    errors = (result for result in results if result is not None)

    return list(errors)


def _rebuild_schema(schema: _Schema) -> Exception | None:
    result: Exception | None
    try:
        schema.model_rebuild()
    except Exception as error:
        result = error
    else:
        result = None

    return result
