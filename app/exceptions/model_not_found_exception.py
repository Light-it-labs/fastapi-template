class ModelNotFoundException(Exception):
    def __init__(self, message="Model not found."):
        self.message = message
        super().__init__(self.message)
