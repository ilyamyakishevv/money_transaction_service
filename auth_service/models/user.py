from typing import TYPE_CHECKING
import uuid
import sys
import os

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
)

from sqlalchemy import Integer, Float, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from common.models.base import Base

if TYPE_CHECKING:
    from transaction_service.models.transaction import Transaction


class User(Base):
    __tablename__ = "user"
    __table_args__ = {'extend_existing': True}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    uid: Mapped[uuid.UUID] = mapped_column(
        UUID, unique=True, index=True, default=uuid.uuid4
    )
    first_name: Mapped[str]
    second_name: Mapped[str]
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String)
    balance: Mapped[float] = mapped_column(
        Float, nullable=False, default=100000.0
    )

    # sended_transactions: Mapped[list["Transaction"]] = relationship(
    #     "Transaction", back_populates="sender"
    # )
    # # received_transactions: Mapped[list["Transaction"]] = relationship(
    # #     "Transaction", back_populates="receiver"
    # # )

    def __repr__(self) -> str:
        return f"<User: {self.first_name} {self.second_name}>"
