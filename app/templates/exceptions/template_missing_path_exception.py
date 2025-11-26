from textwrap import dedent
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.templates import BaseTemplate


class TemplateMissingPathException(Exception):
    def __init__(self, obj: "BaseTemplate") -> None:
        cls_name = obj.__class__.__name__
        self.message = message = dedent(
            f"""
            {cls_name} does not have a path configured.

            Set the path to the template file in the class definition, when
            inheriting from BaseTemplate or BaseEmailTemplate.

            Example:
            ```
            class {cls_name}(BaseTemplate, path="path/to/template.mj"):
                ...
            ```
            """
        )
        super().__init__(message)
