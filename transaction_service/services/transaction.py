from sqlalchemy.ext.asyncio import AsyncSession

from configs.loggers import logger
from common.models import User
from models.transaction import Transaction
from schemas.transaction import TransactionCreateDB
from crud.transaction import crud_transaction


async def send_money_transaction(
    db: AsyncSession,
    receiver: User,
    sender: User,
    amount: float,
) -> Transaction:
    try:
        new_transaction = await crud_transaction.create(
            db=db,
            create_schema=TransactionCreateDB(
                sender_id=sender.id,
                receiver_id=receiver.id,
                amount=amount,
                status="pending",
            ),
        )
        await db.commit()
        if not receiver:
            logger.info("Receive user does not exist!")
            raise ValueError("Receive user does not exist!")

        if sender.balance < amount:
            new_transaction.status = "rejected"
            await db.commit()
            raise ValueError("Not enough money for send!")

        sender.balance -= amount
        receiver.balance += amount
        await db.commit()
        new_transaction.status = "approved"
        await db.commit()
        logger.info(f"Transsaction with id {new_transaction.id} confirmed!")

    except Exception as ex:
        await db.rollback()
        if new_transaction:
            new_transaction.status = "rejected"
            await db.commit()
        logger.info(f"Transsaction with id {new_transaction.id} rejected!")
        raise ValueError(f"Error in transaction proccess: {ex}")

    return new_transaction
