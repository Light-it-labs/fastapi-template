from abc import ABC, abstractmethod
from typing import Any, List


class BaseEmailClient(ABC):
    def __init__(self, client: Any):
        self.client = client

    @abstractmethod
    def send_email(
        self,
        to_emails: List[str],
        html_message: str,
        set_configuration_name: bool = False,
    ) -> Any:
        pass
