__all__ = (
    "add_schema",
    "is_rebuilt",
    "rebuild_schemas",
)

import threading

import pydantic

from . import _exc

# region types
type _Schema = type[pydantic.BaseModel]
type _IsRebuilt = bool
type _Registry = dict[_Schema, _IsRebuilt]


# region public api
def add_schema(schema: _Schema) -> None:
    _registry[schema] = False


def rebuild_schemas() -> None:
    with _rebuilding_mutex:
        _rebuild_schemas()


def is_rebuilt(schema: _Schema) -> _IsRebuilt:
    return _registry[schema]


# region private
_registry: _Registry = {}
_rebuilding_mutex = threading.Lock()


def _rebuild_schemas() -> None:
    errors: list[Exception] = []

    for schema, is_rebuilt in _registry.items():
        if is_rebuilt:
            continue

        try:
            schema.model_rebuild()
        except Exception as error:
            errors.append(error)
        else:
            _registry[schema] = True

    if errors:
        raise _exc.SchemaRebuildFailedErrors(errors)
