class GlobalEmailClientNotSetException(Exception):
    def __init__(self) -> None:
        self.message = (
            "Global email client not set. Call `app.emails.set_client` first."
        )
        super().__init__(self.message)
