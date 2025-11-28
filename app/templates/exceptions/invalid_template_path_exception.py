from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.templates import BaseTemplate


class InvalidTemplatePathException(Exception):
    def __init__(self, obj: "BaseTemplate") -> None:
        cls_name = obj.__class__.__name__
        path = obj.get_path()
        self.message = msg = f"{cls_name}: couldn't find template at {path}."
        super().__init__(msg)
