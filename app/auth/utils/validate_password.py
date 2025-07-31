import re


def validate_password(value: str) -> str:
    if len(value) < 8:
        raise ValueError("Password must be at least 8 characters long")
    if not any(char.isdigit() for char in value):
        raise ValueError("Password must contain at least one digit")
    if not any(char.isupper() for char in value):
        raise ValueError("Password must contain at least one uppercase letter")
    if not any(char.islower() for char in value):
        raise ValueError("Password must contain at least one lowercase letter")
    if not re.search(r"[!@#$%^&*()_+=\-[\]{};:'\"|,.<>/?]", value):
        raise ValueError(
            "Password must contain at least one special character"
        )
    return value
