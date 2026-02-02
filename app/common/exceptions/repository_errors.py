__all__ = (
    "RepositoryError",
    "EntityNotCreatedError",
    "EntityNotDeletedError",
    "EntityNotFoundError",
    "EntityNotUpdatedError",
)

import re
import typing as t

from .base_application_error import BaseApplicationError


class RepositoryError(BaseApplicationError):
    pass


class EntityNotFoundError(RepositoryError):
    def __init__(self, entity: type | str):
        if isinstance(entity, str):
            entity_name = entity
        else:
            entity_name = _separate_camel_case(entity.__name__)
        super().__init__(f"{entity_name} not found")


class EntityNotCreatedError(RepositoryError):
    def __init__(self, entity: type | str):
        if isinstance(entity, str):
            entity_name = entity
        else:
            entity_name = _separate_camel_case(entity.__name__)
        super().__init__(f"{entity_name} not created")


class EntityNotUpdatedError(RepositoryError):
    def __init__(self, entity: type | str):
        if isinstance(entity, str):
            entity_name = entity
        else:
            entity_name = _separate_camel_case(entity.__name__)
        super().__init__(f"{entity_name} not updated")


class EntityNotDeletedError(RepositoryError):
    def __init__(self, entity: type | str):
        if isinstance(entity, str):
            entity_name = entity
        else:
            entity_name = _separate_camel_case(entity.__name__)
        super().__init__(f"{entity_name} not deleted")


# helpers
_CAMEL_CASE_PATTERN: t.Final[re.Pattern] = re.compile(r"(?<=[a-z])(?=[A-Z])")


def _separate_camel_case(s: str) -> str:
    return _CAMEL_CASE_PATTERN.sub(" ", s)
