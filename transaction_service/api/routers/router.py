from fastapi import APIRouter

from api.endpoints.transactions import router as transaction_router

router = APIRouter(prefix="/v1")

router.include_router(
    transaction_router,
    prefix="/transaction",
    tags=["Transations"],
)