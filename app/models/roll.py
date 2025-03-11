from typing import Optional

from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.database import Base


class Roll(Base):
   
    length: Mapped[float] = mapped_column(nullable=False)
    weight: Mapped[float] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False, server_default=func.now())
    removed_at: Mapped[datetime] = mapped_column(nullable=True)
    
