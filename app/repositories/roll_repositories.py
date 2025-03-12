from typing import List, Optional


from app.models.roll import Roll
from app.repositories.interfaces import StorageInterface
from app.schemas.roll import (
    RollCreate,
    RollFilter,
    RollStatistics,
    SRoll,
    StatisticsPeriod,
)


class RollRepository:

    def __init__(self, storage: StorageInterface[Roll, SRoll]):
        self.storage = storage

    async def get(self, roll_id: int) -> Optional[SRoll]:
        return await self.storage.get(roll_id)

    async def get_all(self) -> List[SRoll]:
        return await self.storage.get_all()

    async def create(self, obj_in: RollCreate) -> Optional[SRoll]:
        obj_data = obj_in.model_dump()
        return await self.storage.create(obj_data)

    async def remove_roll(self, roll_id: int) -> Optional[SRoll]:
        return await self.storage.remove_roll(roll_id)

    async def get_filtered(self, filters: RollFilter) -> Optional[List[SRoll]]:
        return await self.storage.get_filtered(filters)

    async def get_statistics_data(self, period: StatisticsPeriod) -> Optional[RollStatistics]:
        return await self.storage.get_statistics_data(Roll, period)
