from sqlalchemy import Integer, String, Date, ForeignKey
from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Shipments(Base):
    __tablename__='shipments'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'))
    shipment_date: Mapped[Date] = mapped_column(type_=Date)
    quantity: Mapped[int]
    supplier_name: Mapped[str] 