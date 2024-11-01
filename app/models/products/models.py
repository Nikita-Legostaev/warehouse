from sqlalchemy import Integer, String, Date, ForeignKey
from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Products(Base):
    __tablename__='products'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    product_name: Mapped[str]
    manufacturer_id: Mapped[int] = mapped_column(ForeignKey('manufacturers.id'))
    category_id: Mapped[int] = mapped_column(ForeignKey('product_categories.id'))
    price: Mapped[int]
    expiration_date: Mapped[Date] = mapped_column(type_=Date)
    weight: Mapped[int]
    stock_id: Mapped[int] = mapped_column(ForeignKey('stock.id'))
    stock_location: Mapped[int]
    stock_quantity: Mapped[int] 