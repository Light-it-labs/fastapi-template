from __future__ import annotations

__all__ = (
    "EntityDefinitionError",
    "MissingDtoError",
    "InvalidDtoError",
)

import typing as t

from . import _utils

if t.TYPE_CHECKING:
    from .entity import Entity
    from .entity import _DtoConstraint


class EntityDefinitionError(Exception):
    pass


class MissingDtoError(EntityDefinitionError):
    def __init__(
        self,
        entity_cls: type[Entity],
        missing_dto_constraint: _DtoConstraint,
    ) -> None:
        dto_name, dto_cls = missing_dto_constraint
        dto_bases = (dto_cls.__name__,)
        model_name, model_bases = _utils.extract_class_info(entity_cls)

        message_lines = (
            f"Missing {dto_name} definition from {model_name} declaration.",
            "",
            "Example:",
            _utils.build_nested_class_definition_example(
                outer_class_name=model_name,
                outer_class_bases=model_bases,
                inner_class_name=dto_name,
                inner_class_bases=dto_bases,
                inner_class_statements=(
                    "# fields required to perform operation via repository",
                ),
            ),
        )
        message = "\n".join(message_lines)
        super().__init__(message)


class InvalidDtoError(EntityDefinitionError):
    def __init__(
        self,
        entity_cls: type[Entity],
        invalid_dto_constraint: _DtoConstraint,
    ) -> None:
        dto_name, dto_cls = invalid_dto_constraint
        dto_bases = (dto_cls.__name__,)
        model_name, model_bases = _utils.extract_class_info(entity_cls)

        message_lines = (
            f"Invalid {dto_name} schema definition, must be child of {dto_cls.__name__}",
            "",
            "Example:",
            _utils.build_nested_class_definition_example(
                outer_class_name=model_name,
                outer_class_bases=model_bases,
                inner_class_name=dto_name,
                inner_class_bases=dto_bases,
                inner_class_statements=(
                    "# fields required to perform operation via repository",
                ),
            ),
        )
        message = "\n".join(message_lines)
        super().__init__(message)
