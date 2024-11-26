from datetime import datetime
from typing import TYPE_CHECKING, Optional
import uuid
import sys
import os

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
)

from sqlalchemy import ForeignKey, Integer, Float, DateTime, func
from sqlalchemy.dialects.postgresql import ENUM, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from transaction_service.constants.transaction import TransactionStatus
from auth_service.models.user import User
from models.base import Base

if TYPE_CHECKING:
    from auth_service.models.user import User


class Transaction(Base):
    __tablename__ = "transaction"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[TransactionStatus] = mapped_column(
        ENUM(TransactionStatus, default=TransactionStatus.PENDING),
    )
    uid: Mapped[uuid.UUID] = mapped_column(
        UUID, unique=True, index=True, default=uuid.uuid4
    )
    transaction_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    sender_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("user.id", ondelete="CASCADE"), index=True
    )
    reciver_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("user.id", ondelete="CASCADE"), index=True
    )
    sender: Mapped[User] = relationship(
        "User", back_populates="sended_transactions"
    )
    reciever: Mapped[User] = relationship(
        "User", back_populates="recieved_transactions"
    )

    def __repr__(self) -> str:
        return f"<Transaction: {self.id} >"
