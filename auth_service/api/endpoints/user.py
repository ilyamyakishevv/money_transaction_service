import uuid

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
from api.dependencies.database import get_async_db
from crud.user import crud_user
from models.user import User
from schemas.user import UserProfileResponse, UserCreate, UserCreateDB
from schemas.token import UserLogin, TokenAccessRefresh
from security.password import hash_password, verify_password
from services.tokens import create_tokens, set_tokens_to_cookie

router = APIRouter()


@router.post("/register/",
            response_model=UserProfileResponse, 
            status_code=status.HTTP_201_CREATED,)
async def create_user(
    create_data: UserCreate,
    db: AsyncSession = Depends(get_async_db),
):
    user = await crud_user.get_by_email(db=db, email=create_data.email)
    if user:
        logger.info(f"User with email {create_data.email} is already registred!")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Email {create_data.email} is already "
            "associated with an account.",
        )
    create_data_dict = create_data.model_dump(exclude_unset=True)
    hashed_password = await hash_password(create_data_dict.pop("password"))
    new_user = await crud_user.create(
        db=db,
        create_schema=UserCreateDB(
            **create_data_dict,
            uid=str(uuid.uuid4()),
            hashed_password=hashed_password,         
        )
    )
    logger.info(f"User with email {create_data.email} registred successfully!")
    return new_user

@router.post("/login/", response_model=TokenAccessRefresh)
async def login(
    user_login: UserLogin, db: AsyncSession = Depends(get_async_db)
):
    found_user = await crud_user.get_by_email(db, email=user_login.email)
    if not found_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_login.email} not found.",
        )

    password_verified = await verify_password(
        plain_password=user_login.password,
        hashed_password=found_user.hashed_password,
    )
    if not password_verified:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User password is wrong",
        )

    tokens = await create_tokens(subject={"uid": str(found_user.uid)})
    response = JSONResponse(content=tokens.model_dump())
    logger.info(f"User with email {found_user.email} login successfully!")
    return await set_tokens_to_cookie(response=response, tokens=tokens)

@router.get("/profile/", response_model=UserProfileResponse)
async def get_profile(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user),
):
    return await crud_user.get_by_uid(
        db=db, uid=current_user.uid
    )

@router.get("/user/{id}/", response_model=UserProfileResponse)
async def get_profile(
    id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user),
):
    return await crud_user.get_by_id(
        db=db, obj_id=id,
    )   
