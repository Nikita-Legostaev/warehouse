from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column

from app.config import settings
from app.exceptions import ConnectionError


async_engine = create_async_engine(
    url=settings.DB_URL
)

AsyncSessionLocal = async_sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    try:
        async with AsyncSessionLocal() as async_session:
            yield async_session
    except SQLAlchemyError:
        raise ConnectionError()


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
