"""inital

Revision ID: 3be7b1e060f9
Revises:
Create Date: 2024-11-21 13:06:58.277651

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "3be7b1e060f9"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("uid", sa.UUID(), nullable=False),
        sa.Column("first_name", sa.String(), nullable=False),
        sa.Column("second_name", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("hashed_password", sa.String(), nullable=False),
        sa.Column("balance", sa.Float(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_user_email"), "user", ["email"], unique=True)
    op.create_index(op.f("ix_user_id"), "user", ["id"], unique=False)
    op.create_index(op.f("ix_user_uid"), "user", ["uid"], unique=True)
    op.create_table(
        "transaction",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("amount", sa.Float(), nullable=False),
        sa.Column(
            "status",
            postgresql.ENUM(
                "pending", "approved", "rejected", name="transactionstatus"
            ),
            nullable=False,
        ),
        sa.Column("uid", sa.UUID(), nullable=False),
        sa.Column(
            "transaction_date",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("sender_id", sa.Integer(), nullable=True),
        sa.Column("reciver_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["reciver_id"], ["user.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["sender_id"], ["user.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_transaction_id"), "transaction", ["id"], unique=False)
    op.create_index(
        op.f("ix_transaction_reciver_id"),
        "transaction",
        ["reciver_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_transaction_sender_id"),
        "transaction",
        ["sender_id"],
        unique=False,
    )
    op.create_index(op.f("ix_transaction_uid"), "transaction", ["uid"], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_transaction_uid"), table_name="transaction")
    op.drop_index(op.f("ix_transaction_sender_id"), table_name="transaction")
    op.drop_index(op.f("ix_transaction_reciver_id"), table_name="transaction")
    op.drop_index(op.f("ix_transaction_id"), table_name="transaction")
    op.drop_table("transaction")
    op.drop_index(op.f("ix_user_uid"), table_name="user")
    op.drop_index(op.f("ix_user_id"), table_name="user")
    op.drop_index(op.f("ix_user_email"), table_name="user")
    op.drop_table("user")
    # ### end Alembic commands ###
