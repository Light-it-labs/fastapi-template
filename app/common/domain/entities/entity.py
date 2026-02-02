__all__ = ("Entity",)

import typing as t

import pydantic

from . import _exc


class _DtoConstraint(t.NamedTuple):
    name: str
    parent_cls: type


type _DtoConstraints = t.Collection[_DtoConstraint]
type _DtoConstraintEvaluation = _exc.EntityDefinitionError | None
type _EntityDefinitionErrors = t.Sequence[_exc.EntityDefinitionError]


# TODO: schema registry and automatic model rebuilding (fix circular imports for good)
# TODO: sentinel for unloaded relationships (fix shape of data problem)
class Entity(pydantic.BaseModel):
    """
    Base model of the application, representing an object in the db.

    :var CreateDto: (required) Subschema for creating an object
    :var UpdateDto: (required) Subschema for updating an object

    ## Example:
    ```
    class User(Entity):
        id: UserId
        name: str
        last_name: str

        class CreateDto(pydantic.BaseModel):
            name: str
            last_name: str

        class UpdateDto(pydantic.BaseModel):
            name: str | None = None
            last_name: str | None = None
    ```
    """

    model_config = pydantic.ConfigDict(
        from_attributes=True,
        frozen=True,
    )

    CreateDto: t.ClassVar[type[pydantic.BaseModel]]
    UpdateDto: t.ClassVar[type[pydantic.BaseModel]]

    @classmethod
    def __pydantic_init_subclass__(cls, **kw: t.Any) -> None:
        super().__pydantic_init_subclass__(**kw)
        cls._validate_entity_definition()

    __required_dtos__: t.Final[_DtoConstraints] = (
        _DtoConstraint("CreateDto", pydantic.BaseModel),
        _DtoConstraint("UpdateDto", pydantic.BaseModel),
    )

    @classmethod
    def _validate_entity_definition(cls) -> None:
        errors = cls._collect_entity_definition_errors()

        if errors:
            msg = f"Can't create {cls.__name__} entity class"
            raise ExceptionGroup(msg, errors)

    @classmethod
    def _collect_entity_definition_errors(cls) -> _EntityDefinitionErrors:
        errors = (
            cls._evaluate_dto_constraint(dto_constraint)
            for dto_constraint in cls.__required_dtos__
        )

        return tuple(error for error in errors if error is not None)

    @classmethod
    def _evaluate_dto_constraint(
        cls,
        dto_constraint: _DtoConstraint,
    ) -> _DtoConstraintEvaluation:
        dto_name, dto_parent_cls = dto_constraint

        if not hasattr(cls, dto_name):
            return _exc.MissingDtoError(cls, dto_constraint)

        dto = getattr(cls, dto_name)
        is_type = isinstance(dto, type)
        is_subclass = is_type and issubclass(dto, dto_parent_cls)

        if not is_subclass:
            return _exc.InvalidDtoError(cls, dto_constraint)

        return None
