import re

from pydantic import BaseModel, Field, validator

MIN_PASSWORD_LENGTH = 8

class PasswordBase(BaseModel):
    password: str = Field(..., min_length=8)

    @validator("password")
    def password_validation(cls, v: str) -> str:
        if len(v) < MIN_PASSWORD_LENGTH and not re.match(r"^[ -~]+$", v):
            msg = "Password does not meet the requirements."
            raise ValueError(msg)
        return v
