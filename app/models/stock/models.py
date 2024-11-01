from sqlalchemy import Integer, String, Date, ForeignKey
from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Stock(Base):
    __tablename__='stock'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    row: Mapped[int]
    cell: Mapped[int]