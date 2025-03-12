import pytest
from datetime import datetime, timezone, timedelta
from app.schemas.roll import RollCreate, RollFilter, StatisticsPeriod


@pytest.mark.asyncio
async def test_repository_get(mock_repository):
    roll = await mock_repository.get(1)
    assert roll is not None
    assert roll.id == 1

    roll = await mock_repository.get(999)
    assert roll is None


@pytest.mark.asyncio
async def test_repository_get_all(mock_repository):
    rolls = await mock_repository.get_all()

    assert rolls is not None
    assert isinstance(rolls, list)
    assert len(rolls) > 0


@pytest.mark.asyncio
async def test_repository_create(mock_repository):
    roll_data = RollCreate(length=175.0, weight=85.0)

    roll = await mock_repository.create(roll_data)

    assert roll is not None
    assert roll.length == roll_data.length
    assert roll.weight == roll_data.weight
    assert roll.created_at is not None
    assert roll.removed_at is None


@pytest.mark.asyncio
async def test_repository_remove_roll(mock_repository):
    roll = await mock_repository.remove_roll(1)

    assert roll is not None
    assert roll.id == 1
    assert roll.removed_at is not None

    roll = await mock_repository.remove_roll(999)
    assert roll is None


@pytest.mark.asyncio
async def test_repository_get_filtered(mock_repository):
    filters = [
        RollFilter(id_min=2),
        RollFilter(weight_min=100.0),
        RollFilter(length_max=200.0),
        RollFilter(is_active=True)
    ]

    for filter_data in filters:
        rolls = await mock_repository.get_filtered(filter_data)

        assert rolls is not None
        assert isinstance(rolls, list)

        if filter_data.id_min is not None:
            for roll in rolls:
                assert roll.id >= filter_data.id_min

        if filter_data.weight_min is not None:
            for roll in rolls:
                assert roll.weight >= filter_data.weight_min

        if filter_data.length_max is not None:
            for roll in rolls:
                assert roll.length <= filter_data.length_max

        if filter_data.is_active is not None:
            for roll in rolls:
                assert roll.is_active == filter_data.is_active


@pytest.mark.asyncio
async def test_repository_get_statistics_data(mock_repository):
    now = datetime.now(timezone.utc)
    period = StatisticsPeriod(
        start_date=now - timedelta(days=10),
        end_date=now
    )

    stats_data = await mock_repository.get_statistics_data(period)

    assert stats_data is not None
    assert "added_count" in stats_data
    assert "removed_count" in stats_data
    assert "stats" in stats_data
    assert "storage_times" in stats_data
    assert "records" in stats_data

    assert stats_data["added_count"] >= 0
    assert stats_data["removed_count"] >= 0
    assert stats_data["stats"] is not None
    assert hasattr(stats_data["stats"], "avg_length")
    assert hasattr(stats_data["stats"], "avg_weight")
    assert hasattr(stats_data["stats"], "total_weight")
