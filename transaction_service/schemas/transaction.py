from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from constants.transaction import TransactionStatus


class TransactionBase(BaseModel):
    amount: float


class TransactionCreate(TransactionBase):
    sender_id: int
    receiver_id: int


class TransactionCreateDB(TransactionCreate):
    id: int
    uid: UUID
    transaction_date: datetime
    status: TransactionStatus = Field(default=TransactionStatus.PENDING)


class TransactionResponse(TransactionBase):
    id: int
    sender_id: int
    reciever_id: int
    status: TransactionStatus
    transaction_date: datetime
