import uuid
import sys
import os

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
)
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from configs.loggers import logger
from api.dependencies.auth import get_current_user
from auth_service.models.user import User
from api.dependencies.database import get_async_db
from crud.transaction import crud_transaction
from models.transaction import Transaction
from schemas.transaction import TransactionResponse, TransactionCreate


router = APIRouter()

@router.get("/sended_transactions/", response_model=TransactionResponse)
async def get_sended_transactions(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    return await crud_transaction.get_by_sender_id(
        db=db, sender_id=current_user.id
    )

@router.get("/recieved_transactions/", response_model=TransactionResponse)
async def get_recieved_transactions(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    return await crud_transaction.get_by_reciver_id(
        db=db, reciever_id=current_user.id
    )