__all__ = ("ExternalProviderError",)


class ExternalProviderError(Exception):
    def __init__(
        self, message: str = "Connection with external provider failed."
    ):
        self.message = message
        super().__init__(self.message)
