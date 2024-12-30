from uuid import UUID
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str


# Contents of JWT token
class TokenPayload(BaseModel):
    user_id: UUID
