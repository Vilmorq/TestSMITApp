from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import async_get_session


async def get_global_session(
    request: Request, session: AsyncSession = Depends(async_get_session)
) -> None:
    request.state.session = session
