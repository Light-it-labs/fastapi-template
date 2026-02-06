from datetime import datetime
from typing import Any, Iterable, Sequence
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.auth.utils import security
from app.two_factor_authentication.use_cases import CreateNewUser2FAUseCase
from app.users.models import User


class UserFactory:
    class _UserConfig(BaseModel):
        id: UUID | None = None
        created_at: datetime | None = None
        email: str = "test@user.com"
        password: str = "password"
        with_2fa: bool = False

    @property
    def config(self) -> type[_UserConfig]:
        return self.__class__._UserConfig

    def __init__(self, session: Session):
        self.session = session
        self._create_2fa_use_case = CreateNewUser2FAUseCase(session)

    def create(
        self,
        config: _UserConfig | None = None,
        /,
        **kw: Any,
    ) -> User:
        if config is None:
            config = self.config(**kw)

        user = self._create_model(config)
        self.session.add(user)
        self.session.flush()

        if config.with_2fa:
            self._create_2fa(user)

        return user

    def create_many(
        self,
        amount: int,
        /,
        *,
        email_base: str = "test@mail.com",
        configurations: Sequence[_UserConfig] | None = None,
        **kw: Any,
    ) -> list[User]:
        assert amount > 1, "Amount must be greater than 1"
        assert email_base.count("@") == 1, (
            "`email_base` must contain exactly one `@`"
        )

        configurations = self._parse_configurations(
            amount, email_base, configurations, kw
        )

        users = [self._create_model(config) for config in configurations]

        self.session.add_all(users)
        self.session.flush()

        self._create_2fa(
            user
            for user, config in zip(users, configurations, strict=True)
            if config.with_2fa
        )

        return users

    def _create_model(self, config: _UserConfig, /) -> User:
        user = User(
            email=config.email,
            hashed_password=security.get_password_hash(config.password),
        )

        if config.id:
            user.id = config.id

        if config.created_at:
            user.created_at = config.created_at

        return user

    def _create_2fa(self, users: User | Iterable[User], /) -> None:
        if isinstance(users, User):
            users = [users]

        for user in users:
            self._create_2fa_use_case.execute(user.id)
            self.session.refresh(
                user, attribute_names=("two_factor_authentications",)
            )
            assert len(user.two_factor_authentications) == 1, (
                "UserFactory failed to create user 2fa"
            )

    def _parse_configurations(
        self,
        amount: int,
        email_base: str,
        configurations: Sequence[_UserConfig] | None,
        kw: dict[str, Any],
    ) -> list[_UserConfig]:
        address, domain = email_base.split("@")

        parsed_configurations = []
        for i in range(amount):
            if configurations is None or len(configurations) <= i:
                config = self.config(**kw)
            else:
                config = configurations[i]

            if "email" not in config.model_fields_set:
                config.email = f"{address}{i}@{domain}"

            parsed_configurations.append(config)

        return parsed_configurations
