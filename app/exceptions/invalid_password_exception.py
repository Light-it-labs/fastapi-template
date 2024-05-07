class InvalidPasswordException(Exception):
    def __init__(self, message="Invalid password."):
        self.message = message
        super().__init__(self.message)
