__all__ = ("BaseApplicationError",)


class BaseApplicationError(Exception):
    """Base exception for all custom exceptions of the application"""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)
