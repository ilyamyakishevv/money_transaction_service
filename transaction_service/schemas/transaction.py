from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from constants.transaction import TransactionStatus


class TransactionBase(BaseModel):
    amount: float

    class Config:
        from_attributes = True


class TransactionCreate(TransactionBase):
    sender_id: int
    receiver_id: int


class TransactionCreateDB(TransactionCreate):
    status: str


class TransactionResponse(TransactionBase):
    id: int
    uid: UUID
    sender_id: int
    receiver_id: int
    status: str
    transaction_date: datetime

    class Config:
        from_attributes = True


class TransactionUpdateDB(TransactionBase):
    pass
