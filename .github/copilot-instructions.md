# Project Coding Standards and Patterns

This document outlines the coding standards, patterns, and best practices to be followed when working on this project.

## Project Structure

The project follows a clean architecture pattern with the following layers:

- `api/`: FastAPI routes and endpoints
- `models/`: Database models using SQLAlchemy
- `schemas/`: Pydantic models for request/response validation
- `services/`: Business logic and service layer
- `repositories/`: Database access layer
- `use_cases/`: Application use cases that orchestrate services
- `exceptions/`: Custom exception classes
- `enums/`: Enumeration classes
- `utils/`: Utility functions and helpers

Each domain (e.g., users, auth, metrics) has its own module following this structure.

### Common Module Structure

The `common/` module contains base classes and shared functionality:

- Base repositories (`BaseRepository`)
- Base models (`Base`)
- Common schemas
- Shared services
- Generic exceptions

## Code Style and Formatting

### Python Version

- Python 3.12 or higher is required
- Use modern Python features and type hints

### Code Formatting

- Use `ruff` for code formatting and linting
- Run `ruff check --fix` and `ruff format` before committing
- Run `mypy .` for type checking

### Import Organization

1. Standard library imports
2. Third-party imports
3. Local application imports
4. Separate imports with a blank line between groups

Example:

```python
from typing import Optional, List
from uuid import UUID

from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session

from app.common.models import Base
from app.users.schemas import UserCreate
```

## API Design Patterns

### Endpoint Structure

- Group related endpoints under a common router
- Use appropriate HTTP methods (GET, POST, PUT, DELETE)
- Include HTTP status codes in decorators
- Use rate limiting for sensitive endpoints

Example:

```python
@router.post("", status_code=status.HTTP_201_CREATED)
@limiter.limit(settings.RATE_LIMIT)
def create_resource(
    session: SessionDependency,
    data: ResourceCreate,
) -> ResourceResponse:
    return CreateResourceUseCase(session).execute(data)
```

### Request/Response Schemas

- Use Pydantic models for all request/response schemas
- Inherit from common base schemas when appropriate
- Use proper field validation and types
- Include model_config for SQLAlchemy model conversion
- All functions should return Pydantic models as responses, not raw database models.

Example:

```python
class ResourceBase(BaseModel):
    name: str
    active: bool

class ResourceCreate(ResourceBase):
    owner_id: UUID

class ResourceInDB(ResourceBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
```

## Testing Patterns

### Test Organization

- Group tests by domain/feature
- Use descriptive test class and method names
- Follow the Arrange-Act-Assert pattern
- Use fixtures for common setup

Example:

```python
class TestResourceEndpoint:
    def test_create_resource_success(
        self,
        client: TestClient,
        session: Session,
    ) -> None:
        # Arrange
        data = {"name": "test", "active": True}

        # Act
        response = client.post("/api/v1/resources", json=data)

        # Assert
        assert response.status_code == 201
```

### Test Fixtures

- Use session fixture for database tests
- Use client fixture for API tests
- Create helper functions in `tests/utils/`

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

- Use SQLAlchemy declarative models
- Inherit from `Base` class
- Use proper column types and constraints
- Include type annotations for all fields

Example:

```python
class Resource(Base):
    __tablename__ = "resources"

    name: Mapped[str] = mapped_column(String(100))
    active: Mapped[bool] = mapped_column(default=True)
    owner_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
```

### Repository Pattern

- Use `BaseRepository` for CRUD operations
- Implement specific repository methods when needed
- Use proper typing with generics
- Follow single responsibility principle

Example:

```python
class ResourcesRepository(
    BaseRepository[Resource, ResourceCreate, ResourceUpdate]
):
    def get_by_owner(
        self,
        db: Session,
        owner_id: UUID,
    ) -> Resource | None:
        return (
            db.query(self.model)
            .filter(self.model.owner_id == owner_id)
            .first()
        )

resources_repository = ResourcesRepository(Resource)
```

## Service Layer Patterns

### Service Implementation

- Services handle business logic
- Use dependency injection for repositories
- Return domain objects (not DB models)
- Handle service-specific exceptions
- When doing a GET operation, if the resource is not found, raise a `ModelNotFoundException` instead of returning `None`.

Example:

```python
class ResourceService:
    def __init__(
        self,
        session: Session,
        repository: ResourcesRepository = resources_repository,
    ):
        self.session = session
        self.repository = repository

    def create_resource(
        self,
        data: ResourceCreate,
    ) -> ResourceInDB:
        resource = self.repository.create(self.session, data)
        return ResourceInDB.model_validate(resource)
```

## Use Case Layer Patterns

### Use Case Implementation

- One use case per specific business action
- Orchestrate multiple services when needed
- Handle use case specific validation
- Return API response objects
- When calling services that may not find a resource, handle the `ModelNotFoundException` appropriately to ensure the use case logic remains clear.
- When calling services always send the data using the correct Pydantic schema.

Example:

```python
class CreateResourceUseCase:
    def __init__(self, session: Session):
        self.session = session
        self.service = ResourceService(self.session)

    def execute(self, data: ResourceCreate) -> ResourceResponse:
        try:
            resource = self.service.create_resource(data)
            return ResourceResponse.model_validate(resource)
        except Exception as e:
            raise ModelNotCreatedException(str(e))
```


### Miscellaneous
- When using timezone.now(), ensure to use pytz.utc for timezone awareness.
- Always follow SOLID principles in your code design.
