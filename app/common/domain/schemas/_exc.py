__all__ = (
    "SchemaNotInstantiableError",
    "SchemaNotRebuiltError",
    "SchemaRebuildFailedErrors",
)

import pydantic

type _Schema = type[pydantic.BaseModel]


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
            f"Call `{base_schema.__name__}.rebuild_all()` before instantiating schemas"
        )
        super().__init__(msg)


class SchemaRebuildFailedErrors(ExceptionGroup):
    def __new__(cls, errors: list[Exception]) -> "SchemaRebuildFailedErrors":
        msg = "Failed to rebuild schemas"
        return super().__new__(cls, msg, errors)
