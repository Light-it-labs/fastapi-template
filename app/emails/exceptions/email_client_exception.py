class EmailClientException(Exception):
    def __init__(self, message: str = "Connection with email client failed."):
        self.message = message
        super().__init__(self.message)
