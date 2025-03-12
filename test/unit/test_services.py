import pytest
from datetime import datetime, timezone, timedelta
from unittest.mock import AsyncMock
from app.schemas.roll import RollCreate, RollFilter, StatisticsPeriod
from app.exceptions import (
    RollNotFoundError,
    CannotAddDataToDatabase,
    CannotDeleteDataFromDatabase
)


@pytest.fixture
def roll_create_data():
    return RollCreate(length=100.0, weight=50.0)


@pytest.fixture
def stats_period():
    now = datetime.now(timezone.utc)
    return StatisticsPeriod(
        start_date=now - timedelta(days=10),
        end_date=now
    )


@pytest.mark.asyncio
async def test_create_roll_success(roll_service, roll_create_data):
    roll = await roll_service.create_roll(roll_create_data)

    assert roll is not None
    assert roll.length == roll_create_data.length
    assert roll.weight == roll_create_data.weight
    assert roll.created_at is not None
    assert roll.removed_at is None


@pytest.mark.asyncio
async def test_create_roll_failure(roll_service, roll_create_data, mock_repository):
    mock_repository.create = AsyncMock(side_effect=CannotAddDataToDatabase())

    with pytest.raises(CannotAddDataToDatabase):
        await roll_service.create_roll(roll_create_data)


@pytest.mark.asyncio
async def test_get_roll_success(roll_service):
    roll = await roll_service.get_roll(1)

    assert roll is not None
    assert roll.id == 1


@pytest.mark.asyncio
async def test_get_roll_not_found(roll_service):
    with pytest.raises(RollNotFoundError):
        await roll_service.get_roll(999)


@pytest.mark.asyncio
async def test_remove_roll_success(roll_service):
    roll = await roll_service.remove_roll(1)

    assert roll is not None
    assert roll.id == 1
    assert roll.removed_at is not None


@pytest.mark.asyncio
async def test_remove_roll_not_found(roll_service):
    with pytest.raises(RollNotFoundError):
        await roll_service.remove_roll(999)


@pytest.mark.asyncio
async def test_remove_roll_db_error(roll_service, mock_repository):
    mock_repository.remove_roll = AsyncMock(side_effect=CannotDeleteDataFromDatabase())

    with pytest.raises(CannotDeleteDataFromDatabase):
        await roll_service.remove_roll(1)


@pytest.mark.asyncio
async def test_get_rolls_all(roll_service):
    rolls = await roll_service.get_rolls()

    assert rolls is not None
    assert len(rolls) > 0


@pytest.mark.asyncio
async def test_get_rolls_filtered(roll_service):
    filter_data = RollFilter(weight_min=100.0)

    rolls = await roll_service.get_rolls(filter_data)

    assert rolls is not None
    for roll in rolls:
        assert roll.weight >= 100.0


@pytest.mark.asyncio
async def test_get_statistics(roll_service, stats_period):
    stats = await roll_service.get_statistics(stats_period)

    assert stats is not None
    assert stats.period_start == stats_period.start_date
    assert stats.period_end == stats_period.end_date
    assert stats.added_rolls_count >= 0
    assert stats.removed_rolls_count >= 0
    assert stats.total_weight > 0
