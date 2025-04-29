from setuptools import Command

from app.db.seeders.db_seeder import DBSeeder
from app.db.seeders.users_seeder import UsersSeeder
from app.db.session import SessionLocal


class SeedUsersCommand(Command):
    description = "Seed patients"
    user_options = []  # type: ignore

    def run(self) -> None:
        """Run the command."""
        session = SessionLocal()
        db_seeder = DBSeeder(session)
        db_seeder.run_seeder(UsersSeeder)

        session.close()

    def initialize_options(self) -> None:
        """Set default values for options."""

    def finalize_options(self) -> None:
        """Finalize options."""
