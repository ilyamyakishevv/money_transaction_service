from typing import Optional, Type, List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


from constants.crud_types import ModelType
from crud.async_crud import BaseAsyncCRUD

from models.transaction import (
    Transaction,
)
from schemas.transaction import TransactionCreateDB, TransactionUpdateDB


class CRUDTransaction(
    BaseAsyncCRUD[Transaction, TransactionCreateDB, TransactionUpdateDB]
):
    def __init__(self, model: Type[ModelType]) -> None:
        super().__init__(model)

    async def get_by_reciver_id(
        self,
        db: AsyncSession,
        *,
        reciever_id: int,
    ) -> Optional[List[Transaction]]:
        statement = select(self.model).where(self.model.receiver_id == reciever_id)
        result = await db.execute(statement)
        return result.scalars().unique().all()

    async def get_by_sender_id(
        self,
        db: AsyncSession,
        *,
        sender_id: int,
    ) -> Optional[List[Transaction]]:
        statement = select(self.model).where(self.model.sender_id == sender_id)
        result = await db.execute(statement)
        return result.unique().scalars().all()

    async def get_all(
        self,
        db: AsyncSession,
    ) -> Optional[List[Transaction]]:
        statement = select(self.model)
        result = await db.execute(statement)
        return result.unique().scalars().all()


crud_transaction = CRUDTransaction(Transaction)
