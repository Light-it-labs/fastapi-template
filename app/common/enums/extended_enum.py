from enum import Enum


class ExtendedEnum(Enum):
    @classmethod
    def list(cls) -> list[str]:
        return list(map(lambda c: c.value, cls))
