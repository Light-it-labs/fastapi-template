__all__ = (
    "build_nested_class_definition_example",
    "extract_class_info",
)

import typing as t


def build_nested_class_definition_example(
    *,
    outer_class_name: str = "Outer",
    outer_class_bases: t.Sequence[str] | None = None,
    inner_class_name: str = "Inner",
    inner_class_bases: t.Sequence[str] | None = None,
    inner_class_statements: t.Sequence[str] = ("# ...",),
) -> str:
    output_lines = (
        _build_class_header(outer_class_name, outer_class_bases),
        _indent(1, _build_class_header(inner_class_name, inner_class_bases)),
        *_indent(2, inner_class_statements),
    )

    return "\n".join(output_lines)


def _build_class_header(name: str, bases: t.Sequence[str] | None) -> str:
    return f"class {name}{f'({", ".join(bases)})' if bases else ''}:"


@t.overload
def _indent(level: int, val: str) -> str: ...
@t.overload
def _indent(level: int, val: t.Sequence[str]) -> t.Sequence[str]: ...


def _indent(level: int, val: str | t.Sequence[str]) -> str | t.Sequence[str]:
    space = "    " * level

    if isinstance(val, str):
        return f"{space}{val}"

    return tuple(f"{space}{line}" for line in val)


class _ClassInfo(t.NamedTuple):
    class_name: str
    class_bases: t.Sequence[str]


def extract_class_info(cls: type) -> _ClassInfo:
    return _ClassInfo(
        class_name=cls.__name__,
        class_bases=tuple(base.__name__ for base in cls.__bases__),
    )
