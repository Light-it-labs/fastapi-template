from abc import ABC, abstractmethod

from app.emails.schema.email import Email


class BaseEmailClient(ABC):
    @abstractmethod
    def send_email(self, /, email: Email) -> None:
        pass
