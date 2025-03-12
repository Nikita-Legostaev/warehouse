from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.roll import Roll
from app.repositories.postgresql import PostgreSQLStorage
from app.repositories.roll_repositories import RollRepository
from app.service.roll_service import RollService


def get_roll_repository(db: AsyncSession = Depends(get_db)) -> RollRepository:
    storage = PostgreSQLStorage(db, Roll)
    return RollRepository(storage)


def get_roll_service(db: AsyncSession = Depends(get_db)) -> RollService:
    repository = get_roll_repository(db)
    return RollService(repository)
