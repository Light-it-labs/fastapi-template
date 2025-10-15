import time
from typing import Any
from urllib.parse import urlparse

import sentry_sdk
from asgi_correlation_id import CorrelationIdMiddleware
from asgi_correlation_id.context import correlation_id
from celery import Celery
from fastapi import FastAPI, Request, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
import structlog
from uvicorn.protocols.utils import get_path_with_query_string


# NOTE: Unconventional import order is needed to control boot up flow
# region Configuration
from app.core.config import settings
from app.celery.celery_settings import get_celery_settings

celery_settings = get_celery_settings()


# region Logging
from app.custom_logging import setup_logging

setup_logging(json_logs=settings.LOG_JSON_FORMAT, log_level=settings.LOG_LEVEL)
access_logger = structlog.stdlib.get_logger("api.access")

if settings.SENTRY_DSN:
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        environment=settings.RUN_ENV,
        send_default_pii=True,
    )


# region Instances
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

celery = Celery(
    settings.SERVER_NAME,
)
celery.config_from_object(celery_settings)


# region Middleware
if settings.RUN_ENV == "local":
    from sqlalchemy.orm import relationship

    relationship.__kwdefaults__["lazy"] = "raise"


if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            str(origin) for origin in settings.BACKEND_CORS_ORIGINS
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.middleware("http")
async def logging_middleware(request: Request, call_next: Any) -> Response:
    structlog.contextvars.clear_contextvars()
    request_id = correlation_id.get()
    structlog.contextvars.bind_contextvars(request_id=request_id)

    start_time = time.perf_counter()
    response = Response(status_code=500)
    try:
        response = await call_next(request)
    except Exception:
        structlog.stdlib.get_logger("api.error").exception(
            "Uncaught exception"
        )
        raise
    finally:
        parsed_url = urlparse(str(request.url))
        if parsed_url.path == "/api/v1/health":
            return response
        process_time = time.perf_counter() - start_time
        status_code = response.status_code
        url = get_path_with_query_string(request.scope)
        if request.client is not None:
            client_host = request.client.host
            client_port = request.client.port
        else:
            client_host = "unknown"
            client_port = 12345
        http_method = request.method
        http_version = request.scope["http_version"]

        access_logger.info(
            f"""{client_host}:{client_port} - "{http_method} {url}
             HTTP/{http_version}" {status_code}""",
            http={
                "url": str(request.url),
                "status_code": status_code,
                "method": http_method,
                "request_id": request_id,
                "version": http_version,
            },
            network={"client": {"ip": client_host, "port": client_port}},
            duration=process_time,
        )
        response.headers["X-Process-Time"] = str(process_time / 10**9)
        return response


app.add_middleware(CorrelationIdMiddleware)


# region Exceptions
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    modified_details = []
    details = exc.errors()
    for error in details:
        modified_details.append(
            {
                "loc": error["loc"],
                "message": error["msg"],
                "type": error["type"],
            }
        )
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": modified_details}),
    )


# region Routers
# NOTE: its important to import routers last as this action
#       triggers import of the use case layer all the way down
#       to the model definitions.
from app.users.api.routers import api_router as users_router
from app.two_factor_authentication.api.router import (
    api_router as two_factor_authentication_router,
)
from app.auth.api.routers import api_router as auth_router
from app.common.api.routers import api_router as common_router

app.include_router(users_router, prefix=settings.API_V1_STR)
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(common_router, prefix=settings.API_V1_STR)
app.include_router(
    two_factor_authentication_router, prefix=settings.API_V1_STR
)
