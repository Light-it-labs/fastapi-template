class ModelNotCreatedException(Exception):
    def __init__(self, message="Model not created."):
        self.message = message
        super().__init__(self.message)
