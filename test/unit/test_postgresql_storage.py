import pytest
from datetime import datetime, timezone, timedelta
from unittest.mock import AsyncMock, MagicMock, patch
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.postgresql import PostgreSQLStorage
from app.models.roll import Roll
from app.schemas.roll import RollFilter, StatisticsPeriod


class TestPostgreSQLStorage:

    @pytest.fixture
    def mock_session(self):
        session = AsyncMock(spec=AsyncSession)
        return session

    @pytest.fixture
    def storage(self, mock_session):
        return PostgreSQLStorage(mock_session, Roll)

    @pytest.mark.asyncio
    async def test_get(self, storage, mock_session):
        test_roll = Roll()
        test_roll.id = 1
        test_roll.length = 150.0
        test_roll.weight = 75.0
        test_roll.created_at = datetime.now(timezone.utc)

        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = test_roll

        mock_session.execute.return_value = test_roll

        with patch.object(storage.session, 'execute', AsyncMock(return_value=mock_result)):
            result = await storage.get(1)

            assert result == test_roll

    @pytest.mark.asyncio
    async def test_get_all(self, storage, mock_session):
        test_rolls = []
        for i in range(1, 4):
            roll = Roll()
            roll.id = i
            roll.length = 100.0 * i
            roll.weight = 50.0 * i
            roll.created_at = datetime.now(timezone.utc)
            test_rolls.append(roll)

        mock_result = MagicMock()
        mock_scalars = MagicMock()
        mock_result.scalars.return_value = mock_scalars
        mock_scalars.all.return_value = test_rolls

        with patch.object(storage.session, 'execute', AsyncMock(return_value=mock_result)):
            result = await storage.get_all()

            assert result == test_rolls

    @pytest.mark.asyncio
    async def test_create(self, storage, mock_session):
        obj_data = {"length": 150.0, "weight": 75.0}

        with patch.object(storage.session, 'commit', AsyncMock()), \
                patch.object(storage.session, 'refresh', AsyncMock()):
            result = await storage.create(obj_data)

            assert isinstance(result, Roll)
            assert result.length == 150.0
            assert result.weight == 75.0

            mock_session.add.assert_called_once()
            mock_session.commit.assert_called_once()
            mock_session.refresh.assert_called_once()

    @pytest.mark.asyncio
    async def test_remove_roll(self, storage, mock_session):
        test_roll = Roll()
        test_roll.id = 1
        test_roll.length = 150.0
        test_roll.weight = 75.0
        test_roll.created_at = datetime.now(timezone.utc)
        test_roll.removed_at = None

        with patch.object(storage, 'get', AsyncMock(side_effect=[test_roll, test_roll])), \
                patch.object(storage.session, 'execute', AsyncMock()), \
                patch.object(storage.session, 'commit', AsyncMock()):

            result = await storage.remove_roll(1)

            assert result == test_roll
            assert storage.session.execute.called
            assert storage.session.commit.called

            with patch.object(storage, 'get', AsyncMock(return_value=None)):
                result = await storage.remove_roll(999)
                assert result is None

            test_roll.removed_at = datetime.now(timezone.utc)
            with patch.object(storage, 'get', AsyncMock(return_value=test_roll)):
                result = await storage.remove_roll(1)
                assert result == test_roll
                assert storage.session.execute.called

    @pytest.mark.asyncio
    async def test_get_filtered(self, storage, mock_session):
        test_rolls = []
        for i in range(1, 4):
            roll = Roll()
            roll.id = i
            roll.length = 100.0 * i
            roll.weight = 50.0 * i
            roll.created_at = datetime.now(timezone.utc)
            test_rolls.append(roll)

        mock_result = MagicMock()
        mock_scalars = MagicMock()
        mock_result.scalars.return_value = mock_scalars
        mock_scalars.all.return_value = test_rolls

        filters = [
            RollFilter(id_min=2),
            RollFilter(weight_min=100.0),
            RollFilter(length_max=200.0),
            RollFilter(is_active=True),
            RollFilter(created_at_min=datetime.now(timezone.utc) - timedelta(days=1)),
            RollFilter(removed_at_max=datetime.now(timezone.utc))
        ]

        for filter_data in filters:
            with patch.object(storage.session, 'execute', AsyncMock(return_value=mock_result)):
                result = await storage.get_filtered(filter_data)

                assert result == test_rolls

    @pytest.mark.asyncio
    async def test_get_statistics_data(self, storage, mock_session):
        now = datetime.now(timezone.utc)
        period = StatisticsPeriod(
            start_date=now - timedelta(days=10),
            end_date=now
        )

        added_mock = MagicMock()
        added_mock.scalar.return_value = 5

        removed_mock = MagicMock()
        removed_mock.scalar.return_value = 2

        class MockStats:
            avg_length = 150.0
            min_length = 100.0
            max_length = 300.0
            avg_weight = 65.0
            min_weight = 50.0
            max_weight = 150.0
            total_weight = 250.0

        stats_mock = MagicMock()
        stats_mock.first.return_value = MockStats()

        class MockStorageTimes:
            min_storage_time = timedelta(days=1)
            max_storage_time = timedelta(days=5)

        storage_mock = MagicMock()
        storage_mock.first.return_value = MockStorageTimes()

        test_rolls = []
        for i in range(1, 4):
            roll = Roll()
            roll.id = i
            roll.length = 100.0 * i
            roll.weight = 50.0 * i
            roll.created_at = datetime.now(timezone.utc) - timedelta(days=5)
            test_rolls.append(roll)

        records_mock = MagicMock()
        records_mock.scalars.return_value.all.return_value = test_rolls

        with patch.object(
            storage.session, 'execute',
            AsyncMock(side_effect=[added_mock, removed_mock, stats_mock, storage_mock, records_mock])
        ):
            result = await storage.get_statistics_data(Roll, period)

            assert result["added_count"] == 5
            assert result["removed_count"] == 2
            assert result["stats"].avg_length == 150.0
            assert result["stats"].total_weight == 250.0
            assert result["storage_times"].min_storage_time == timedelta(days=1)
            assert result["storage_times"].max_storage_time == timedelta(days=5)
            assert result["records"] == test_rolls
