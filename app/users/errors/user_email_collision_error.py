__all__ = ("UserEmailCollisionError",)

from app.common.exceptions import BaseApplicationError


class UserEmailCollisionError(BaseApplicationError):
    def __init__(self, email: str):
        self.email = email
        msg = "User with that email already registered."
        super().__init__(msg)
