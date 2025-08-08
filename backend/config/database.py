from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase
from urllib.parse import quote_plus
from config.config import settings

ASYNC_SQLALCHEMY_DATABASE_URL = (
    f'mysql+asyncmy://{settings.db_username}:{quote_plus(settings.db_password)}@'
    f'{settings.db_host}:{settings.db_port}/{settings.db_database}'
)

async_engine = create_async_engine(
    ASYNC_SQLALCHEMY_DATABASE_URL,
    echo=settings.db_echo,
    max_overflow=settings.db_max_overflow,
    pool_size=settings.db_pool_size,
    pool_recycle=settings.db_pool_recycle,
    pool_timeout=settings.db_pool_timeout,
)
AsyncSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=async_engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass
