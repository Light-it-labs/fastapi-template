from typing import Any

from sqlalchemy.orm import Session


class DBSeeder:
    def __init__(self, db: Session):
        self.db = db

    def run_seeder(self, seeder: Any) -> None:
        seeder.run(self.db)
