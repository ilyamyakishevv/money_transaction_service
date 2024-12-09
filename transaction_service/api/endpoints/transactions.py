import sys
import os
from typing import List

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
)
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from fastapi_filter import FilterDepends
from sqlalchemy.ext.asyncio import AsyncSession

from api.filters.filters import TransactionFilter
from configs.loggers import logger
from auth_service.api.dependencies.auth import get_current_user
from auth_service.crud.user import crud_user
from common.models import User
from api.dependencies.database import get_async_db
from crud.transaction import crud_transaction
from schemas.transaction import TransactionResponse
from services.transaction import send_money_transaction

router = APIRouter()


@router.get("/sended_transactions/", response_model=List[TransactionResponse])
async def get_sended_transactions(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user),
):
    return await crud_transaction.get_by_sender_id(db=db, sender_id=current_user.id)


@router.get("/recieved_transactions/", response_model=TransactionResponse)
async def get_recieved_transactions(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user),
):
    return await crud_transaction.get_by_reciver_id(db=db, reciever_id=current_user.id)


@router.get("/all_transactions/", response_model=List[TransactionResponse])
async def get_all_transactions(
    filters: TransactionFilter = FilterDepends(TransactionFilter),
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user),
):  
    logger.info(f"User with ID {current_user.id} just seen transactions list!")
    return await crud_transaction.get_all(db=db, filters=filters)


@router.post("/make_transaction/{receiver_id}/")
async def make_transaction(
    receiver_id: int,
    amount: float,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user),
):
    sender = await crud_user.get_by_id(db=db, obj_id=current_user.id)
    receiver = await crud_user.get_by_id(db=db, obj_id=receiver_id)
    if not receiver: 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {receiver_id} not found.",
        )

    return await send_money_transaction(
        db=db,
        sender=sender,
        receiver=receiver,
        amount=amount,
    )


@router.get("/transaction/{id}/", response_model=TransactionResponse)
async def get_transaction_by_id(id: int, db: AsyncSession = Depends(get_async_db)):
    return await crud_transaction.get_by_id(db=db, obj_id=id)
