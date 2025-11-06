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
    ) -> requests.Response | None:
        try:
            response = requests.request(
                method=method,
                url=(
                    f"{self.base_url}{endpoint}" if self.base_url else endpoint
                ),
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

        except requests.exceptions.RequestException as error:
            logger.error(str(endpoint))
            logger.error(str(error))
            logger.error(str(data))
            logger.error(str(params))
            logger.error(
                f"response: {error.response.text if error.response else None}"
            )
            return None
