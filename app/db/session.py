from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

if settings.MODE == "TEST":
    DATABASE_URL = settings.TEST_DATABASE_URL
    DATABASE_PARAMS = {"poolclass": NullPool}
else:
    DATABASE_URL = settings.DATABASE_URL
    DATABASE_PARAMS = {}

engine = create_async_engine(settings.DATABASE_URL, **DATABASE_PARAMS)

# async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

