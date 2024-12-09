from typing import Optional, Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


from constants.crud_types import ModelType
from crud.async_crud import BaseAsyncCRUD

from auth_service.models.user import (
    User,
)
from auth_service.schemas.user import UserCreateDB, UserUpdateDB


class CRUDUser(BaseAsyncCRUD[User, UserCreateDB, UserUpdateDB]):
    def __init__(self, model: Type[ModelType]) -> None:
        super().__init__(model)

    async def get_by_email(self, db: AsyncSession, *, email: str) -> Optional[User]:
        statement = select(self.model).where(self.model.email == email.lower())
        result = await db.execute(statement)
        return result.scalars().first()


crud_user = CRUDUser(User)
