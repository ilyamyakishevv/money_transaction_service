from typing import Union, Optional, List
from uuid import UUID


from pydantic import BaseModel
from pydantic.class_validators import validator

from common.schemas.password import PasswordBase


class UserBase(BaseModel):
    first_name: str
    second_name: str
    email: str

    class Config:
        from_attributes = True


class UserCreate(PasswordBase, UserBase):
    pass


class UserCreateDB(UserBase):
    uid: UUID
    hashed_password: str

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    email: Optional[str]


class UserUpdateDB(UserUpdate):
    pass


class UserProfileResponse(UserBase):
    uid: UUID
    balance: float
