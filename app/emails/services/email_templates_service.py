from __future__ import annotations

from enum import Enum
from typing import Any, ClassVar, Literal, TypedDict, Unpack, overload

from jinja2 import Environment, FileSystemLoader


class EmailTemplate(Enum):
    WELCOME = "welcome.j2"
    OTHER = "_base.j2"


class _WelcomeKwargs(TypedDict):
    name: str


class _OtherKwargs(TypedDict):
    pass


class EmailTemplatesService:
    _instance: ClassVar[EmailTemplatesService | None] = None
    _environment: ClassVar[Environment]

    def __new__(cls) -> EmailTemplatesService:
        if cls._instance:
            return cls._instance

        cls._environment = Environment(
            loader=FileSystemLoader("app/emails/templates"),
        )

        cls._instance = super().__new__(cls)
        return cls._instance

    @overload
    def render(
        self,
        template: Literal[EmailTemplate.WELCOME],
        **kw: Unpack[_WelcomeKwargs],
    ) -> str: ...
    @overload
    def render(
        self,
        template: Literal[EmailTemplate.OTHER],
        **kw: Unpack[_OtherKwargs],
    ) -> str: ...

    def render(self, template: EmailTemplate, **kw: Any) -> str:
        jinja_template = self._environment.get_template(template.value)
        return jinja_template.render(**kw)
