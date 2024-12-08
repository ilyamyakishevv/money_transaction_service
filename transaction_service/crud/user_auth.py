from typing import Optional
from uuid import UUID
import sys
import os

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
)


from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

async def get_by_uid(db: AsyncSession, *, uid: UUID):
    from auth_service.models.user import User 
    statement = select(User).where(
        User.uid == uid,
    )
    result = await db.execute(statement)
    return result.scalars().first()
