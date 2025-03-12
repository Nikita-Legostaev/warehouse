import pytest
from datetime import datetime, timezone, timedelta
from unittest.mock import AsyncMock
from app.models.roll import Roll
from app.repositories.roll_repositories import RollRepository
from app.service.roll_service import RollService


@pytest.fixture
def mock_storage():
    storage = AsyncMock()

    test_rolls = {}
    for i in range(1, 4):
        roll = Roll()
        roll.id = i
        roll.length = 100.0 * i
        roll.weight = 50.0 * i
        roll.created_at = datetime.now(timezone.utc) - timedelta(days=10 - i)
        roll.removed_at = None if i != 2 else datetime.now(timezone.utc)
        test_rolls[i] = roll

    async def mock_get(id):
        return test_rolls.get(id)

    async def mock_get_all():
        return list(test_rolls.values())

    async def mock_create(obj_data):
        new_id = max(test_rolls.keys(), default=0) + 1
        roll = Roll()
        roll.id = new_id
        roll.length = obj_data.get("length", 0)
        roll.weight = obj_data.get("weight", 0)
        roll.created_at = datetime.now(timezone.utc)
        roll.removed_at = None
        test_rolls[new_id] = roll
        return roll

    async def mock_remove_roll(roll_id):
        if roll_id in test_rolls:
            roll = test_rolls[roll_id]
            roll.removed_at = datetime.now(timezone.utc)
            return roll
        return None

    async def mock_get_filtered(criteria):
        results = []
        for roll in test_rolls.values():
            if ((criteria.id_min is None or roll.id >= criteria.id_min) and
                (criteria.id_max is None or roll.id <= criteria.id_max)
                and (criteria.weight_min is None or roll.weight >= criteria.weight_min)
                and (criteria.weight_max is None or roll.weight <= criteria.weight_max)
                and (criteria.length_min is None or roll.length >= criteria.length_min)
                and (criteria.length_max is None or roll.length <= criteria.length_max)
                    and (criteria.is_active is None or roll.is_active == criteria.is_active)):
                results.append(roll)
        return results

    async def mock_get_statistics_data(model, period):
        class MockStats:
            avg_length = 150.0
            min_length = 100.0
            max_length = 300.0
            avg_weight = 65.0
            min_weight = 50.0
            max_weight = 150.0
            total_weight = 250.0

        class MockStorageTimes:
            min_storage_time = timedelta(days=1)
            max_storage_time = timedelta(days=5)

        filtered_rolls = []
        for roll in test_rolls.values():
            if (roll.created_at <= period.end_date
                    and (roll.removed_at is None or roll.removed_at >= period.start_date)):
                filtered_rolls.append(roll)

        return {
            "added_count": len([r for r in filtered_rolls if r.created_at >= period.start_date]),
            "removed_count": len([r for r in filtered_rolls if r.removed_at
                                 and r.removed_at >= period.start_date
                                 and r.removed_at <= period.end_date]),
            "stats": MockStats(),
            "storage_times": MockStorageTimes(),
            "records": filtered_rolls
        }

    storage.get.side_effect = mock_get
    storage.get_all.side_effect = mock_get_all
    storage.create.side_effect = mock_create
    storage.remove_roll.side_effect = mock_remove_roll
    storage.get_filtered.side_effect = mock_get_filtered
    storage.get_statistics_data.side_effect = mock_get_statistics_data

    return storage


@pytest.fixture
def mock_repository(mock_storage):
    return RollRepository(mock_storage)


@pytest.fixture
def roll_service(mock_repository):
    return RollService(mock_repository)
