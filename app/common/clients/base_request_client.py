from abc import ABC

import requests
import structlog

from app.core.config import settings

logger = structlog.get_logger(__name__)


class BaseRequestClient(ABC):
    base_url: str | None = None

    def _make_request(
        self,
        *,
        endpoint: str,
        method: str,
        headers: dict | None = None,
        data: dict | str | None = None,
        files: list | None = None,
        params: dict | None = None,
        auth: tuple[str, str] | None = None,
        json: dict | None = None,
        error_message: str | None = None,
    ) -> requests.Response | None:
        url = f"{self.base_url}{endpoint}" if self.base_url else endpoint

        try:
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                data=data,
                files=files,
                params=params,
                auth=auth,
                timeout=settings.REQUESTS_TIMEOUT_SECONDS,
                json=json,
            )
            response.raise_for_status()
            return response

        except requests.exceptions.RequestException as exc:
            message = error_message or self._get_error_message(exc, url)
            logger.error(message)
            return None

    def _get_error_message(
        self,
        exc: requests.exceptions.RequestException,
        url: str,
    ) -> str:
        msg_data = {"url": url, "exception": exc}

        if exc.response:
            msg_data["response"] = exc.response.text

        return f"{self.__class__}: request failed. Data: {msg_data}"
