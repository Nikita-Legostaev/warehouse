from datetime import datetime, timezone
from typing import Any, Dict, Generic, List, Optional, TypeVar

from sqlalchemy import DateTime, and_, cast, func, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.interfaces import StorageInterface
from app.schemas.roll import RollFilter

T = TypeVar('T')
S = TypeVar('S')


class PostgreSQLStorage(Generic[T, S]):

    def __init__(self, session: AsyncSession, model_class):
        self.session = session
        self.model = model_class

    async def get(self, id: Any) -> Optional[S]:
        query = select(self.model).where(self.model.id == id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_all(self) -> Optional[List[S]]:
        query = select(self.model)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def create(self, obj_data: Dict[str, Any]) -> S:
        db_obj = self.model(**obj_data)
        self.session.add(db_obj)
        await self.session.commit()
        await self.session.refresh(db_obj)
        return db_obj

    async def remove_roll(self, roll_id: int) -> Optional[S]:
        db_obj = await self.get(roll_id)
        if not db_obj:
            return None

        if hasattr(db_obj, 'removed_at') and getattr(db_obj, 'removed_at') is not None:
            return db_obj

        update_data = {"removed_at": datetime.now(timezone.utc)}
        query = (update(self.model)
                 .where(self.model.id == roll_id)
                 .values(**update_data)
                 )

        await self.session.execute(query)
        await self.session.commit()

        return await self.get(roll_id)

    def _filter_by_id(self, query, criteria):
        if criteria.id_min is not None:
            query = query.filter(self.model.id >= criteria.id_min)
        if criteria.id_max is not None:
            query = query.filter(self.model.id <= criteria.id_max)
        return query

    def _filter_by_weight(self, query, criteria):
        if criteria.weight_min is not None:
            query = query.filter(self.model.weight >= criteria.weight_min)
        if criteria.weight_max is not None:
            query = query.filter(self.model.weight <= criteria.weight_max)
        return query

    def _filter_by_length(self, query, criteria):
        if criteria.length_min is not None:
            query = query.filter(self.model.length >= criteria.length_min)
        if criteria.length_max is not None:
            query = query.filter(self.model.length <= criteria.length_max)
        return query

    def _filter_by_created_at(self, query, criteria):
        if criteria.created_at_min is not None:
            query = query.filter(
                cast(self.model.created_at, DateTime(timezone=True))
                >= cast(criteria.created_at_min, DateTime(timezone=True))
            )
        if criteria.created_at_max is not None:
            query = query.filter(
                cast(self.model.created_at, DateTime(timezone=True))
                <= cast(criteria.created_at_max, DateTime(timezone=True))
            )
        return query

    def _filter_by_removed_at(self, query, criteria):
        if criteria.removed_at_min is not None:
            query = query.filter(
                or_(
                    cast(self.model.removed_at, DateTime(timezone=True))
                    >= cast(criteria.removed_at_min, DateTime(timezone=True)),
                    self.model.removed_at.is_(None)
                )
            )
        if criteria.removed_at_max is not None:
            query = query.filter(
                or_(
                    cast(self.model.removed_at, DateTime(timezone=True))
                    <= cast(criteria.removed_at_max, DateTime(timezone=True)),
                    self.model.removed_at.is_(None)
                )
            )
        return query

    def _filter_by_active_status(self, query, criteria):
        if criteria.is_active is not None:
            if criteria.is_active:
                query = query.filter(self.model.removed_at.is_(None))
            else:
                query = query.filter(self.model.removed_at.isnot(None))
        return query

    async def get_filtered(self, criteria: Any) -> Optional[List[S]]:
        if isinstance(criteria, RollFilter):
            query = select(self.model)

            query = self._filter_by_id(query, criteria)
            query = self._filter_by_weight(query, criteria)
            query = self._filter_by_length(query, criteria)
            query = self._filter_by_created_at(query, criteria)
            query = self._filter_by_removed_at(query, criteria)
            query = self._filter_by_active_status(query, criteria)

            result = await self.session.execute(query)
            return list(result.scalars().all())

        query = select(self.model)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_statistics_data(self, model, period) -> Optional[S]:
        start_date = period.start_date.astimezone(timezone.utc)
        end_date = period.end_date.astimezone(timezone.utc)

        period_filter = and_(
            cast(model.created_at, DateTime(timezone=True)) <= cast(end_date, DateTime(timezone=True)),
            or_(
                model.removed_at.is_(None),
                cast(model.removed_at, DateTime(timezone=True)) >= cast(start_date, DateTime(timezone=True))
            )
        )

        added_query = select(func.count(model.id)).filter(
            cast(model.created_at, DateTime(timezone=True)) >= cast(start_date, DateTime(timezone=True)),
            cast(model.created_at, DateTime(timezone=True)) <= cast(end_date, DateTime(timezone=True))
        )
        added_result = await self.session.execute(added_query)
        added_count = added_result.scalar() or 0

        removed_query = select(func.count(model.id)).filter(
            cast(model.removed_at, DateTime(timezone=True)) >= cast(start_date, DateTime(timezone=True)),
            cast(model.removed_at, DateTime(timezone=True)) <= cast(end_date, DateTime(timezone=True))
        )
        removed_result = await self.session.execute(removed_query)
        removed_count = removed_result.scalar() or 0

        stats_query = select(
            func.avg(model.length).label("avg_length"),
            func.min(model.length).label("min_length"),
            func.max(model.length).label("max_length"),
            func.avg(model.weight).label("avg_weight"),
            func.min(model.weight).label("min_weight"),
            func.max(model.weight).label("max_weight"),
            func.sum(model.weight).label("total_weight")
        ).filter(period_filter)

        stats_result = await self.session.execute(stats_query)
        stats = stats_result.first()

        storage_query = select(
            func.min(model.removed_at - model.created_at).label("min_storage_time"),
            func.max(model.removed_at - model.created_at).label("max_storage_time")
        ).filter(
            model.removed_at.isnot(None),
            cast(model.created_at, DateTime(timezone=True)) >= cast(start_date, DateTime(timezone=True)),
            cast(model.removed_at, DateTime(timezone=True)) <= cast(end_date, DateTime(timezone=True))
        )

        storage_result = await self.session.execute(storage_query)
        storage_times = storage_result.first()

        all_records_query = select(model).filter(
            cast(model.created_at, DateTime(timezone=True)) <= cast(end_date, DateTime(timezone=True)),
            or_(
                model.removed_at.is_(None),
                cast(model.removed_at, DateTime(timezone=True)) >= cast(start_date, DateTime(timezone=True))
            )
        )
        records_result = await self.session.execute(all_records_query)
        records = records_result.scalars().all()

        return {
            "added_count": added_count,
            "removed_count": removed_count,
            "stats": stats,
            "storage_times": storage_times,
            "records": records
        }
