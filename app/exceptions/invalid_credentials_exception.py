class InvalidCredentialsException(Exception):
    def __init__(self, message: str = "Invalid credentials"):
        self.message = message
        super().__init__(self.message)
