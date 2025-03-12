from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel, ValidationInfo, field_validator, model_validator


class RollBase(BaseModel):
    length: float
    weight: float


class RollCreate(RollBase):
    pass


class SRoll(RollBase):
    id: int
    created_at: datetime
    removed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class RollFilter(BaseModel):
    id_min: Optional[int] = None
    id_max: Optional[int] = None
    weight_min: Optional[float] = None
    weight_max: Optional[float] = None
    length_min: Optional[float] = None
    length_max: Optional[float] = None
    created_at_min: Optional[datetime] = None
    created_at_max: Optional[datetime] = None
    removed_at_min: Optional[datetime] = None
    removed_at_max: Optional[datetime] = None
    is_active: Optional[bool] = None

    @model_validator(mode='after')
    def validate_ranges(self) -> 'RollFilter':
        for field_name, value in self.model_dump().items():
            if field_name.endswith('_min') and value is not None:
                max_field = field_name.replace('_min', '_max')
                max_value = getattr(self, max_field, None)
                if max_value is not None and value > max_value:
                    raise ValueError(f"Минимальное значение {field_name} не может быть больше максимального")
        return self


class StatisticsPeriod(BaseModel):
    start_date: datetime
    end_date: datetime

    @field_validator('end_date')
    def validate_end_date(cls, v: datetime, info: ValidationInfo) -> datetime:
        start_date = info.data.get('start_date')
        if start_date is not None and v < start_date:
            raise ValueError("Конечная дата не может быть раньше начальной")
        return v

    @field_validator('start_date', 'end_date')
    def ensure_timezone(cls, v: datetime) -> datetime:
        if v.tzinfo is None:
            return v.replace(tzinfo=timezone.utc)
        return v


class RollStatistics(BaseModel):
    period_start: datetime
    period_end: datetime
    added_rolls_count: int
    removed_rolls_count: int
    average_length: Optional[float] = None
    average_weight: Optional[float] = None
    min_length: Optional[float] = None
    max_length: Optional[float] = None
    min_weight: Optional[float] = None
    max_weight: Optional[float] = None
    total_weight: float
    min_storage_time: Optional[float] = None
    max_storage_time: Optional[float] = None
    min_rolls_day: Optional[datetime] = None
    min_rolls_count: Optional[int] = None
    max_rolls_day: Optional[datetime] = None
    max_rolls_count: Optional[int] = None
    min_weight_day: Optional[datetime] = None
    min_weight_total: Optional[float] = None
    max_weight_day: Optional[datetime] = None
    max_weight_total: Optional[float] = None
