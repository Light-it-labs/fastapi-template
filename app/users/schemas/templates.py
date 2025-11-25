from typing import ClassVar

from app import templates


class NewUserTemplate(templates.BaseEmailTemplate):
    path: ClassVar = "test.mjml"

    name: str
