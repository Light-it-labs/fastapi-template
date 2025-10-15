from abc import ABC, abstractmethod


class BaseEmailClient(ABC):
    @abstractmethod
    def send_email(
        self,
        to_emails: list[str],
        html_message: str,
    ) -> None:
        pass
