from typing import Sequence
from uuid import UUID, uuid4

from sqlalchemy.orm import Session

from app.auth.utils import security
from app.users.models.user import User
from app.users.services.users_service import UsersService


class UserFactory:
    def __init__(self, session: Session):
        self.session = session
        self.service = UsersService(session)

    def create(
        self,
        *,
        id: UUID | None = None,
        email: str = "test@user.com",
        password: str = "password",
    ) -> User:
        if id is None:
            id = uuid4()

        user = User(
            id=id,
            email=email,
            hashed_password=security.get_password_hash(password),
        )

        self.session.add(user)
        self.session.flush()
        return user

    def create_many(
        self,
        amount: int,
        *,
        email_base: str = "test@user.com",
        ids: Sequence[UUID] | None,
        emails: Sequence[str] | None = None,
        passwords: Sequence[str] | None = None,
    ) -> list[User]:
        assert amount > 1, "Amount must be greater than 1"

        if ids is not None:
            assert len(ids) == amount, "Wrong number of ids"
        else:
            ids = [uuid4() for _ in range(amount)]

        if emails is not None:
            assert len(emails) == amount, "Wrong number of emails"
        else:
            assert email_base.count("@") == 1, (
                "`email_base` must contain one `@`"
            )
            address, domain = email_base.split("@")
            emails = [f"{address}{i}@{domain}" for i in range(amount)]

        if passwords is not None:
            assert len(passwords) == amount, "Wrong number of passwords"
        else:
            passwords = ["password" for _ in range(amount)]

        users = [
            self.create(id=id, email=email, password=password)
            for id, email, password in zip(ids, emails, passwords, strict=True)
        ]

        return users
