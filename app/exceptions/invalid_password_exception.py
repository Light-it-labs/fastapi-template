class InvalidPasswordException(Exception):
    def __init__(self, message: str = "Invalid password."):
        self.message = message
        super().__init__(self.message)
