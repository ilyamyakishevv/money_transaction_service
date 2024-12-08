from uuid import UUID


import sys
import os

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../"))
)

from fastapi import Depends, HTTPException, Security, status
from fastapi_jwt import JwtAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from crud.user_auth import get_by_uid
from common.databases.database import get_async_session
from auth_service.models.user import User
from auth_service.schemas.token import TokenPayload
from auth_service.security.token import access_security


async def get_current_user(
    credentials: JwtAuthorizationCredentials = Security(access_security),
    db: AsyncSession = Depends(get_async_session),
) -> User:
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
        )
    try:
        token_user = TokenPayload(**credentials.subject)
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        ) from ex
    return await get_user(db=db, user_uid=token_user.uid)


async def get_user(
    db: AsyncSession,
    user_uid: UUID,
) -> User:
    user = await get_by_uid(db, uid=user_uid)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return user
