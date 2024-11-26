from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.user import User


async def get_by_uid(db: AsyncSession, *, uid: UUID) -> Optional[User]:
    statement = select(User).where(
        User.uid == uid,
    )
    result = await db.execute(statement)
    return result.scalars().first()
