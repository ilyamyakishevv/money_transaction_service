import enum


class TransactionStatus(enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"
