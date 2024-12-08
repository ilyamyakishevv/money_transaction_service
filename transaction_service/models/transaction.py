from datetime import datetime
from typing import TYPE_CHECKING, Optional
import uuid
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from sqlalchemy import ForeignKey, Integer, Float, DateTime, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from transaction_service.constants.transaction import TransactionStatus

# from auth_service.models.user import User
from common.models.base import Base

if TYPE_CHECKING:
    from auth_service.models.user import User


class Transaction(Base):
    __tablename__ = "transaction"
    __table_args__ = {"extend_existing": True}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[str] = mapped_column(String)
    uid: Mapped[uuid.UUID] = mapped_column(
        UUID, unique=True, index=True, default=uuid.uuid4
    )
    transaction_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    sender_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("user.id", ondelete="CASCADE"), index=True
    )
    receiver_id: Mapped[Optional[int]] = mapped_column(Integer, index=True)
    # sender: Mapped["User"] = relationship(
    #     "User", back_populates="sended_transactions"
    # )
    # # receiver: Mapped["User"] = relationship(
    # #     "User", back_populates="received_transactions"
    # # )

    def __repr__(self) -> str:
        return f"<Transaction: {self.id} >"
