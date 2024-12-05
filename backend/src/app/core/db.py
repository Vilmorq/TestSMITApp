from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass, sessionmaker

from app.core.settings.base import settings
from app.core.settings.db import db_settings


class Base(DeclarativeBase, MappedAsDataclass):
    pass


async_engine = create_async_engine(
    db_settings.db_url, echo=settings.DEBUG, future=True, pool_size=10
)

local_session = sessionmaker(
    bind=async_engine, class_=AsyncSession, expire_on_commit=False
)


async def async_get_session() -> AsyncSession:
    async_session = local_session
    async with async_session() as session:
        yield session
