# Project Coding Standards and Patterns

This document outlines the coding standards, patterns, and best practices to be followed when working on this FastAPI project.

## Project Structure

The project follows a clean architecture pattern with clear separation of concerns:

### Domain Module Structure

Each domain (e.g., `users/`, `auth/`, `two_factor_authentication/`) follows this layered structure:

- `api/`: FastAPI routes, endpoints, and API-specific dependencies
  - `endpoints.py`: Route handlers
  - `routers.py`: Router configuration
  - `dependencies/`: API-specific dependency injection (e.g., `get_current_user.py`)
- `models/`: SQLAlchemy database models
- `schemas/`: Pydantic models for request/response validation
- `services/`: Business logic and domain service layer
- `repositories/`: Database access and query layer
- `use_cases/`: Application use cases that orchestrate services
- `exceptions/`: Domain-specific exception classes
- `enums/`: Domain enumeration classes
- `utils/`: Domain utility functions and helpers
- `constants/`: Domain constants (e.g., max lengths, defaults)

### Common Module Structure

The `common/` module contains base classes and shared functionality used across all domains:

- `api/dependencies/`: Shared API dependencies (e.g., `get_session.py` for SessionDependency)
- `models/base_class.py`: Base SQLAlchemy model with common fields (id, created_at, updated_at)
- `repositories/base_repository.py`: Generic CRUD repository with type generics
- `schemas/`: Common schemas (e.g., `pagination_schema.py` for ListFilter/ListResponse)
- `exceptions/`: Generic exceptions (ModelNotFoundException, ModelNotCreatedException, ExternalProviderException)
- `enums/extended_enum.py`: Base enum class with helper methods
- `clients/`: Base client classes for external services

### Core Infrastructure

- `core/`: Application configuration and settings
  - `config.py`: Pydantic Settings with environment validation
- `db/`: Database session management
  - `session.py`: SQLAlchemy SessionLocal factory
  - `base.py`: Import all models for Alembic migrations
- `celery/`: Background task configuration
  - `celery_settings.py`: Celery configuration
  - `tasks/`: Celery task definitions
- `emails/`: Email service abstraction layer
  - `clients/`: Email client implementations (Mailpit, etc.)
  - `services/`: Email service with business logic
  - `templates/`: Email template rendering
- `alembic/`: Database migration management

## Code Style and Formatting

### Python Version

- Python 3.12 or higher is required (currently 3.13.8)
- Use modern Python features and type hints extensively

### Code Formatting Tools

- Use `ruff` for code formatting and linting (configured in `pyproject.toml`)
- Run `ruff check --fix` to automatically fix linting issues
- Run `ruff format` to format code before committing
- Run `mypy .` for static type checking
- Configure pre-commit hooks for automated checks

### Type Hints

- All function signatures must include type hints for parameters and return types
- Use `Mapped[Type]` for SQLAlchemy model fields
- Use `Type | None` instead of `Optional[Type]` (PEP 604 union syntax)
- Use generic types where applicable: `list[str]`, `dict[str, int]`, etc.
- Use `Annotated` for FastAPI dependencies

### Import Organization

Organize imports in the following order with blank lines between groups:

1. Standard library imports
2. Third-party library imports (FastAPI, SQLAlchemy, Pydantic, etc.)
3. Local application imports

Within each group, order imports alphabetically.

Example:

```python
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.common.api.dependencies.get_session import SessionDependency
from app.common.exceptions.model_not_found_exception import ModelNotFoundException
from app.users.schemas.user_schema import UserCreate, UserResponse
from app.users.use_cases.create_user_use_case import CreateUserUseCase
```

### Naming Conventions

- **Files**: Use snake_case (e.g., `users_service.py`, `get_current_user.py`)
- **Classes**: Use PascalCase (e.g., `UsersService`, `UserInDB`)
- **Functions/Methods**: Use snake_case (e.g., `get_by_email`, `create_user`)
- **Constants**: Use UPPER_SNAKE_CASE (e.g., `USER_EMAIL_MAX_LENGTH`, `API_V1_STR`)
- **Type Variables**: Use descriptive names with Type suffix (e.g., `ModelType`, `CreateSchemaType`)
- **Pydantic Schemas**: Use descriptive suffixes
  - `*Request`: For API request bodies
  - `*Response`: For API responses
  - `*Create`: For repository create operations
  - `*Update`: For repository update operations
  - `*InDB`: For database model representations

### Code Organization

- Keep line length to 79 characters (configured in ruff)
- Use meaningful variable names
- One class per file (exceptions: small related enums)
- Group related functionality in modules

## API Design Patterns

### Endpoint Structure

- Group related endpoints under a common router (defined in `routers.py`)
- Define endpoint handlers in `endpoints.py`
- Use appropriate HTTP methods (GET, POST, PUT, PATCH, DELETE)
- Always include explicit HTTP status codes in decorators
- Use rate limiting for authentication and sensitive endpoints
- Use dependency injection via FastAPI's `Depends` or `Annotated` types

Example:

```python
from typing import Annotated
from fastapi import APIRouter, Request, Response, status
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.common.api.dependencies.get_session import SessionDependency
from app.core.config import get_settings
from app.users.schemas.user_schema import CreateUserRequest, UserResponse
from app.users.use_cases.create_user_use_case import CreateUserUseCase

router = APIRouter()
settings = get_settings()
limiter = Limiter(key_func=get_remote_address)


@router.post("", status_code=status.HTTP_201_CREATED)
@limiter.limit(settings.RATE_LIMIT)
def create_user(
    request: Request,
    session: SessionDependency,
    data: CreateUserRequest,
) -> UserResponse:
    return CreateUserUseCase(session).execute(data)
```

### Dependency Injection

- Use `Annotated` types for reusable dependencies
- Define common dependencies in `app/common/api/dependencies/`
- Define domain-specific dependencies in each domain's `api/dependencies/`
- Always commit/rollback sessions in dependencies

Common dependencies example:

```python
from typing import Annotated, Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import SessionLocal


def get_session() -> Generator:
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


SessionDependency = Annotated[Session, Depends(get_session)]
```

Domain-specific dependency example:

```python
from typing import Annotated

from fastapi import Depends

from app.users.schemas.user_schema import UserInDB
from app.users.services.users_service import UsersService


def get_current_user(
    session: SessionDependency,
    token: TokenDep,
) -> UserInDB:
    # Authentication logic here
    ...


CurrentUser = Annotated[UserInDB, Depends(get_current_user)]
```

### Request/Response Schemas

- Use Pydantic v2 models for all request/response schemas
- Inherit from `BaseModel` 
- Use proper field validation with Pydantic validators
- Include `model_config = ConfigDict(from_attributes=True)` for schemas that convert from ORM models
- **All API endpoints must return Pydantic models as responses, never raw database models**
- Separate request schemas from database schemas

Schema examples:

```python
from uuid import UUID
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    email: EmailStr


class CreateUserRequest(UserBase):
    """Schema for API request"""
    password: str = Field(min_length=8)


class UserCreate(UserBase):
    """Schema for repository/database operations"""
    hashed_password: str


class UserInDB(UserBase):
    """Schema representing database model"""
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    hashed_password: str


class UserResponse(UserBase):
    """Schema for API response"""
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
```

### Error Handling in Endpoints

- Catch specific exceptions from use cases
- Convert domain exceptions to appropriate HTTP exceptions
- Use proper HTTP status codes
- Provide clear error messages

```python
from fastapi import HTTPException, status

from app.common.exceptions.model_not_found_exception import (
    ModelNotFoundException,
)


@router.get("/{user_id}")
def get_user(user_id: UUID, session: SessionDependency) -> UserResponse:
    try:
        return GetUserUseCase(session).execute(user_id)
    except ModelNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
```

## Testing Patterns

### Test Organization

- Group tests by domain/feature in `tests/<domain>/`
- Mirror the application structure in tests
- Use descriptive test class and method names
- Follow the Arrange-Act-Assert (AAA) pattern
- Use fixtures for common setup and dependency injection

Example:

```python
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


class TestUserEndpoints:
    def test_create_user_success(
        self,
        client: TestClient,
        session: Session,
    ) -> None:
        # Arrange
        user_data = {
            "email": "test@example.com",
            "password": "SecurePass123",
        }

        # Act
        response = client.post("/api/v1/users", json=user_data)

        # Assert
        assert response.status_code == 201
        assert response.json()["email"] == user_data["email"]

    def test_create_user_duplicate_email(
        self,
        client: TestClient,
        session: Session,
    ) -> None:
        # Arrange
        existing_user = create_user(session, "test@example.com")
        user_data = {"email": "test@example.com", "password": "Pass123"}

        # Act
        response = client.post("/api/v1/users", json=user_data)

        # Assert
        assert response.status_code == 409
        assert "already registered" in response.json()["detail"]
```

### Test Fixtures

All test fixtures should be defined in `conftest.py` files:

- `session`: Database session fixture with transaction rollback
- `client`: FastAPI TestClient with overridden dependencies
- Create helper functions in `tests/utils/` for common test data creation

Example `conftest.py`:

```python
from typing import Generator
import pytest
from sqlalchemy import event
from fastapi.testclient import TestClient

from app.common.api.dependencies.get_session import get_session
from app.db.session import engine, SessionLocal
from app.main import app


@pytest.fixture()
def session() -> Generator:
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionLocal(bind=connection)

    # Begin nested transaction for test isolation
    nested = connection.begin_nested()

    @event.listens_for(session, "after_transaction_end")
    def end_savepoint(session, transaction):
        nonlocal nested
        if not nested.is_active:
            nested = connection.begin_nested()

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture()
def client(session) -> Generator:
    def override_get_session():
        yield session

    app.dependency_overrides[get_session] = override_get_session

    with TestClient(app) as client:
        yield client
```

### Test Helpers

Create utility functions in `tests/utils/` for common operations:

```python
from uuid import UUID
from sqlalchemy.orm import Session

from app.users.models.user import User
from app.users.schemas.user_schema import UserCreate
from app.users.repositories.users_repository import users_repository


def create_user(
    session: Session,
    email: str = "test@example.com",
    hashed_password: str = "hashed_password",
) -> User:
    """Helper function to create test users"""
    user_data = UserCreate(email=email, hashed_password=hashed_password)
    return users_repository.create(session, user_data)
```

## Error Handling

### Exception Hierarchy

1. Use custom exceptions for domain-specific errors
2. Inherit from base Exception class
3. Include descriptive error messages
4. Handle exceptions at the appropriate layer

### Custom Exceptions

```python
class ModelNotFoundException(Exception):
    def __init__(self, message: str = "Model not found."):
        self.message = message
        super().__init__(self.message)
```

### Exception Handling in APIs

```python
@router.post("")
def create_resource(data: ResourceCreate) -> ResourceResponse:
    try:
        return use_case.execute(data)
    except ModelNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
    except ModelNotCreatedException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=e.message,
        )
```

## Database Patterns

### Model Definition

- Use SQLAlchemy 2.0+ declarative models
- Inherit from `Base` class (from `app.common.models.base_class`)
- Use `Mapped[Type]` type annotations for all columns
- Use `mapped_column()` for column definitions
- Define proper constraints (unique, foreign keys, indexes)
- All models automatically include: `id` (UUID), `created_at`, `updated_at`

Example:

```python
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import String
from sqlalchemy import ForeignKey
from uuid import UUID

from app.common.models.base_class import Base
from app.users.constants.user_constants import USER_EMAIL_MAX_LENGTH


class User(Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(
        String(USER_EMAIL_MAX_LENGTH),
        unique=True,
        index=True,
    )
    hashed_password: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)


class Profile(Base):
    __tablename__ = "profiles"

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
    )
    display_name: Mapped[str | None] = mapped_column(String(100))
```

### Base Model Features

The `Base` class provides:

- Automatic UUID primary key (`id`)
- Timestamp fields (`created_at`, `updated_at`)
- Proper naming conventions for constraints
- Type annotation mapping (UUID → SQLA_UUID, datetime → DateTime with timezone)

### Constants for Models

Define model constraints in a `constants/` module:

```python
# app/users/constants/user_constants.py
USER_EMAIL_MAX_LENGTH: int = 255
USER_PASSWORD_MIN_LENGTH: int = 8
```

### Repository Pattern

- Use `BaseRepository` for standard CRUD operations
- Create domain-specific repositories for custom queries
- Use proper typing with generics (`ModelType`, `CreateSchemaType`, `UpdateSchemaType`)
- Always work with Pydantic schemas, not raw dictionaries
- Create a singleton instance of each repository

Example:

```python
from uuid import UUID
from sqlalchemy.orm import Session

from app.common.repositories.base_repository import BaseRepository
from app.users.models.user import User
from app.users.schemas.user_schema import UserCreate, UserUpdate


class UsersRepository(
    BaseRepository[User, UserCreate, UserUpdate]
):
    def get_by_email(
        self,
        db: Session,
        email: str,
    ) -> User | None:
        return (
            db.query(self.model)
            .filter(self.model.email == email)
            .first()
        )

    def get_active_users(self, db: Session) -> list[User]:
        return (
            db.query(self.model)
            .filter(self.model.is_active == True)
            .all()
        )


# Create singleton instance
users_repository = UsersRepository(User)
```

### Pagination

Use `ListFilter` and `ListResponse` from common schemas:

```python
from app.common.schemas.pagination_schema import ListFilter, ListResponse

# In repository
def list(
    self,
    db: Session,
    list_options: ListFilter,
) -> ListResponse:
    query = db.query(self.model).filter(self.model.is_active == True)
    return super().list(db, list_options, query)
```

## Service Layer Patterns

### Service Implementation

- Services contain business logic and domain rules
- Use dependency injection for repositories
- Return Pydantic schemas (not raw DB models)
- Handle service-specific exceptions
- **When a GET operation doesn't find a resource, return `None` - let use cases decide how to handle it**
- Always validate and transform data appropriately

Example:

```python
from uuid import UUID
from sqlalchemy.orm import Session

from app.users.repositories.users_repository import (
    UsersRepository,
    users_repository,
)
from app.users.schemas.user_schema import UserCreate, UserInDB


class UsersService:
    def __init__(
        self,
        session: Session,
        repository: UsersRepository = users_repository,
    ):
        self.session = session
        self.repository = repository

    def get_by_email(self, email: str) -> UserInDB | None:
        user = self.repository.get_by_email(self.session, email.lower())
        if not user:
            return None
        return UserInDB.model_validate(user)

    def get_by_id(self, user_id: UUID) -> UserInDB | None:
        user = self.repository.get(self.session, user_id)
        if not user:
            return None
        return UserInDB.model_validate(user)

    def create_user(self, user: UserCreate) -> UserInDB:
        created_user = self.repository.create(self.session, user)
        return UserInDB.model_validate(created_user)
```

### Service Best Practices

1. **Input Validation**: Services receive Pydantic schemas, not raw dictionaries
2. **Data Transformation**: Convert database models to Pydantic schemas using `model_validate()`
3. **Business Logic**: Implement domain rules (e.g., lowercasing emails)
4. **Error Handling**: Return `None` for not found, let use cases handle exceptions
5. **Dependency Injection**: Accept repository instances with sensible defaults

## Use Case Layer Patterns

### Use Case Implementation

- One use case per specific business action
- Orchestrate multiple services when needed
- Handle use case-specific validation and business rules
- Return API response schemas (Pydantic models)
- Convert `None` from services to appropriate exceptions or responses
- Transform service schemas to API response schemas

Example:

```python
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.auth.utils import security
from app.users.schemas.user_schema import (
    CreateUserRequest,
    UserCreate,
    UserResponse,
)
from app.users.services.users_service import UsersService


class CreateUserUseCase:
    def __init__(self, session: Session):
        self.session = session
        self.users_service = UsersService(self.session)

    def execute(self, request: CreateUserRequest) -> UserResponse:
        # Check for existing user
        if self.users_service.get_by_email(request.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with that email already registered.",
            )

        # Transform request to service schema
        user_create = UserCreate(
            email=request.email.lower(),
            hashed_password=security.get_password_hash(request.password),
        )

        # Create user via service
        created_user = self.users_service.create_user(user_create)

        # Trigger background tasks
        from app.celery.tasks.emails import send_welcome_email
        send_welcome_email.delay(created_user.id)

        # Return API response schema
        return UserResponse(
            id=created_user.id,
            email=created_user.email,
        )
```

### Use Case Best Practices

1. **Single Responsibility**: Each use case handles one specific action
2. **Schema Transformation**: Convert between API request/response and service schemas
3. **Business Rules**: Implement high-level validation (e.g., duplicate checks)
4. **Exception Handling**: Convert service `None` returns to appropriate HTTP exceptions
5. **Orchestration**: Coordinate multiple services and trigger side effects
6. **Return Types**: Always return Pydantic response schemas, never raw models


### Miscellaneous
- When using timezone.now(), ensure to use pytz.utc for timezone awareness.
- Always follow SOLID principles in your code design.

## Celery Background Tasks

### Task Definition

- Define tasks in `app/celery/tasks/` directory
- Use `@celery.task` decorator for all background tasks
- Always create new session for each task
- Close sessions in `finally` block to ensure cleanup
- Use retry configuration for tasks that might fail

Example:

```python
from uuid import UUID
from app.db.session import SessionLocal
from app.main import celery
from app.core.config import get_settings
from app.users.services.users_service import UsersService
from app.emails.services.emails_service import EmailService
from app.emails.exceptions.email_client_exception import EmailClientException

settings = get_settings()


@celery.task(
    autoretry_for=(EmailClientException,),
    retry_backoff=settings.SEND_WELCOME_EMAIL_RETRY_BACKOFF_VALUE,
    max_retries=settings.SEND_WELCOME_EMAIL_MAX_RETRIES,
    retry_jitter=False,
)
def send_welcome_email(user_id: UUID) -> None:
    session = SessionLocal()
    try:
        user = UsersService(session).get_by_id(user_id)
        if user:
            EmailService().send_new_user_email(user)
    finally:
        session.close()
```

### Task Best Practices

1. **Session Management**: Always create new sessions in tasks, never reuse
2. **Error Handling**: Use `autoretry_for` for transient failures
3. **Type Hints**: Include type hints, but use `# type: ignore` for Celery's delay method
4. **Idempotency**: Design tasks to be safely retried
5. **Cleanup**: Use `finally` blocks to ensure session closure

## Configuration and Settings

### Settings Pattern

- Use Pydantic Settings for configuration management
- Define all environment variables in `app/core/config.py`
- Use validators for complex configuration logic
- Create singleton using `@lru_cache` decorator
- Use `frozen=True` to make settings immutable

Example:

```python
from functools import lru_cache
from pydantic import field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=".env",
        env_file_encoding="utf-8",
        frozen=True,
    )
    
    # Application settings
    RUN_ENV: str = "local"
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str
    SERVER_NAME: str
    SERVER_HOST: str
    
    # Database settings
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: str | None = None
    
    @field_validator("SQLALCHEMY_DATABASE_URI", mode="before")
    @classmethod
    def assemble_db_uri(cls, field_value: Any, info: ValidationInfo) -> str:
        if isinstance(field_value, str):
            return field_value
        return PostgresDsn.build(
            scheme="postgresql+psycopg2",
            username=info.data.get("POSTGRES_USER"),
            password=info.data.get("POSTGRES_PASSWORD"),
            host=info.data.get("POSTGRES_SERVER"),
            port=info.data.get("POSTGRES_PORT"),
            path=info.data.get("POSTGRES_DB"),
        ).unicode_string()


@lru_cache()
def get_settings() -> Settings:
    return Settings()
```

### Settings Usage

```python
from app.core.config import get_settings

settings = get_settings()
```

## Logging and Middleware

### Structured Logging

- Use `structlog` for all logging
- Include request IDs for tracing
- Log access and errors separately
- Use JSON format for production environments

Example:

```python
import structlog

access_logger = structlog.stdlib.get_logger("api.access")
error_logger = structlog.stdlib.get_logger("api.error")

# In middleware
access_logger.info(
    "request completed",
    http_method=http_method,
    url=url,
    status_code=status_code,
    process_time=process_time,
)
```

### Middleware Patterns

- Use middleware for cross-cutting concerns
- Add correlation ID for request tracing
- Log all requests and responses
- Handle CORS appropriately based on environment

Example from `main.py`:

```python
from asgi_correlation_id import CorrelationIdMiddleware
from asgi_correlation_id.context import correlation_id
import structlog

app.add_middleware(CorrelationIdMiddleware)


@app.middleware("http")
async def logging_middleware(request: Request, call_next: Any) -> Response:
    structlog.contextvars.clear_contextvars()
    request_id = correlation_id.get()
    structlog.contextvars.bind_contextvars(request_id=request_id)

    start_time = time.perf_counter()
    try:
        response = await call_next(request)
        return response
    except Exception:
        error_logger.exception("Uncaught exception")
        raise
    finally:
        process_time = time.perf_counter() - start_time
        # Log request details
```

## Enum Patterns

### Extended Enum

- Inherit from `ExtendedEnum` for common enum functionality
- Use for status values, types, and constants
- Provides `list()` method to get all values

Example:

```python
from app.common.enums.extended_enum import ExtendedEnum


class ClaimsEnum(ExtendedEnum):
    USER_ID = "user_id"
    TWO_FACTOR_USER_ID = "two_factor_user_id"


# Usage
all_claims = ClaimsEnum.list()  # Returns: ["user_id", "two_factor_user_id"]
```

## Email Service Patterns

### Email Client Abstraction

- Use client pattern for email services
- Support multiple email providers (Mailpit for local, others for production)
- Set client globally using dependency injection
- Use templates for email content

Example from `main.py`:

```python
from app import emails

if settings.RUN_ENV == "local":
    email_client = emails.MailpitEmailClient()
else:
    email_client = emails.ProductionEmailClient()

emails.set_client(email_client)
```
