from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column

from app.config import settings

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
    async_session = AsyncSessionLocal()
    try:
        yield async_session
    finally:
        await async_session.close()


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    __name__: str

    __allow_unmapped__ = True

    @declared_attr
    def __tablename__(self) -> str:
        return self.__name__.lower()