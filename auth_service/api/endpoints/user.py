from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies.auth import get_current_user
from api.dependencies.database import get_async_db
from crud.user import crud_user
from models.user import User
from schemas.user import UserProfileResponse, UserCreate

router = APIRouter()


@router.post("/register/",
            response_model=UserProfileResponse, 
            status_code=status.HTTP_201_CREATED,)
async def create_user(
    create_data: UserCreate,
    db: AsyncSession = Depends(get_async_db),
):
    user = await crud_user.get_by_email(db, email=create_data.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Email {create_data.email} is already "
            "associated with an account.",
        )
    new_user = await crud_user.create(
        db=db,
        create_data=create_data,
    
    )
    return new_user

@router.get("/profile/", response_model=UserProfileResponse)
async def get_profile(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user),
):
    return await crud_user.get_by_uid(
        db=db, user_uid=current_user.uid
    )

