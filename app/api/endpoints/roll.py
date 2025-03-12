from typing import List, Optional

from fastapi import APIRouter, Depends

from app.dependencies import get_roll_service
from app.schemas.roll import (
    RollCreate,
    RollFilter,
    RollStatistics,
    SRoll,
    StatisticsPeriod,
)
from app.service.roll_service import RollService

router = APIRouter()


@router.post("/", response_model=Optional[SRoll])
async def create_roll(
    roll_data: RollCreate,
    service: RollService = Depends(get_roll_service)
):
    return await service.create_roll(roll_data)


@router.get("/{roll_id}", response_model=Optional[SRoll])
async def get_roll(
    roll_id: int,
    service: RollService = Depends(get_roll_service)
):
    return await service.get_roll(roll_id)


@router.delete("/{roll_id}", response_model=Optional[SRoll])
async def remove_roll(
    roll_id: int,
    service: RollService = Depends(get_roll_service)
):
    return await service.remove_roll(roll_id)


@router.get("/", response_model=Optional[List[SRoll]])
async def get_rolls(
    filters: RollFilter = Depends(),
    service: RollService = Depends(get_roll_service)
):
    return await service.get_rolls(filters)


@router.post("/statistics", response_model=Optional[RollStatistics])
async def get_statistics(
    period: StatisticsPeriod,
    service: RollService = Depends(get_roll_service)
):
    return await service.get_statistics(period)
