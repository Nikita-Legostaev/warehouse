from datetime import timedelta, timezone
from typing import Any, Dict, List, Optional

from app.exceptions import (
    CannotAddDataToDatabase,
    CannotDeleteDataFromDatabase,
    FilterError,
    RollNotFoundError,
    StatisticsError,
)
from app.repositories.roll_repositories import RollRepository
from app.schemas.roll import (
    RollCreate,
    RollFilter,
    RollStatistics,
    SRoll,
    StatisticsPeriod,
)


class RollService:

    def __init__(self, repository: RollRepository):
        self.repository = repository

    async def create_roll(self, roll_data: RollCreate) -> Optional[SRoll]:
        try:
            return await self.repository.create(roll_data)
        except CannotAddDataToDatabase as e:
            raise CannotAddDataToDatabase()

    async def get_roll(self, roll_id: int) -> Optional[SRoll]:
        roll = await self.repository.get(roll_id)
        if roll is None:
            raise RollNotFoundError()
        return roll

    async def remove_roll(self, roll_id: int) -> Optional[SRoll]:
        try:
            roll = await self.repository.get(roll_id)
            if not roll:
                raise RollNotFoundError()

            return await self.repository.remove_roll(roll_id)
        except CannotDeleteDataFromDatabase:
            raise CannotDeleteDataFromDatabase()

    async def get_rolls(self, filters: Optional[RollFilter] = None) -> List[SRoll]:
        try:
            if filters:
                return await self.repository.get_filtered(filters)
            else:
                return await self.repository.get_all()
        except FilterError:
            raise FilterError()

    async def get_statistics(self, period: StatisticsPeriod) -> Optional[RollStatistics]:
        try:

            data = await self.repository.get_statistics_data(period)

            stats = data["stats"]
            storage_times = data["storage_times"]

            min_storage_time = None
            max_storage_time = None
            if storage_times and storage_times.min_storage_time:
                min_storage_time = storage_times.min_storage_time.total_seconds()
            if storage_times and storage_times.max_storage_time:
                max_storage_time = storage_times.max_storage_time.total_seconds()

            daily_stats = await self._get_daily_statistics(period, data["records"])

            return RollStatistics(
                period_start=period.start_date,
                period_end=period.end_date,
                added_rolls_count=data["added_count"],
                removed_rolls_count=data["removed_count"],
                average_length=stats.avg_length if stats else None,
                average_weight=stats.avg_weight if stats else None,
                min_length=stats.min_length if stats else None,
                max_length=stats.max_length if stats else None,
                min_weight=stats.min_weight if stats else None,
                max_weight=stats.max_weight if stats else None,
                total_weight=stats.total_weight or 0 if stats else 0,
                min_storage_time=min_storage_time,
                max_storage_time=max_storage_time,
                **daily_stats
            )
        except StatisticsError:
            raise StatisticsError()

    async def _get_daily_statistics(self, period: StatisticsPeriod, rolls: List[SRoll]) -> Dict[str, Any]:
        result = {
            "min_rolls_day": None,
            "min_rolls_count": None,
            "max_rolls_day": None,
            "max_rolls_count": None,
            "min_weight_day": None,
            "min_weight_total": None,
            "max_weight_day": None,
            "max_weight_total": None
        }

        if not rolls:
            return result

        start_day = period.start_date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_day = (period.end_date.replace(hour=23, minute=59, second=59, microsecond=999999)
                   + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)

        daily_stats = {}

        current_day = start_day
        while current_day < end_day:
            next_day = current_day + timedelta(days=1)
            daily_stats[current_day] = {
                "count": 0,
                "total_weight": 0
            }
            current_day = next_day

        for roll in rolls:
            created_at = roll.created_at.astimezone(timezone.utc)
            removed_at = roll.removed_at.astimezone(timezone.utc) if roll.removed_at else None

            roll_start_day = max(created_at, period.start_date).replace(hour=0, minute=0, second=0, microsecond=0)
            roll_end_day = min(
                removed_at if removed_at else period.end_date,
                period.end_date
            ).replace(hour=23, minute=59, second=59, microsecond=999999)

            current_day = roll_start_day
            while current_day <= roll_end_day:
                day_key = current_day.replace(hour=0, minute=0, second=0, microsecond=0)
                if day_key in daily_stats:
                    daily_stats[day_key]["count"] += 1
                    daily_stats[day_key]["total_weight"] += roll.weight
                current_day = (current_day + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)

        min_count = float('inf')
        max_count = 0
        min_weight = float('inf')
        max_weight = 0

        for day, stats in daily_stats.items():
            if stats["count"] < min_count and stats["count"] > 0:
                min_count = stats["count"]
                result["min_rolls_day"] = day
                result["min_rolls_count"] = min_count

            if stats["count"] > max_count:
                max_count = stats["count"]
                result["max_rolls_day"] = day
                result["max_rolls_count"] = max_count

            if stats["total_weight"] < min_weight and stats["total_weight"] > 0:
                min_weight = stats["total_weight"]
                result["min_weight_day"] = day
                result["min_weight_total"] = min_weight

            if stats["total_weight"] > max_weight:
                max_weight = stats["total_weight"]
                result["max_weight_day"] = day
                result["max_weight_total"] = max_weight

        if min_count == float('inf'):
            result["min_rolls_day"] = None
            result["min_rolls_count"] = None

        if min_weight == float('inf'):
            result["min_weight_day"] = None
            result["min_weight_total"] = None

        return result
