__all__ = (
    "SchemaNotInstantiableError",
    "SchemaNotRebuiltError",
)

import pydantic

_Schema = type[pydantic.BaseModel]


class SchemaNotInstantiableError(Exception):
    def __init__(self, base_schema: _Schema) -> None:
        msg = (
            f"Class `{base_schema.__name__}` is a base class. "
            "It should not be instantiated"
        )
        super().__init__(msg)


class SchemaNotRebuiltError(Exception):
    def __init__(self, base_schema: _Schema, schema: _Schema) -> None:
        msg = (
            f"Schema not rebuilt: {schema.__name__}\n"
            f"Call `{base_schema.__name__}.rebuild_schemas()` before instantiating schemas"
        )
        super().__init__(msg)
