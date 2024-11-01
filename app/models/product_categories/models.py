from sqlalchemy import Integer, String, Date, ForeignKey
from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Product_categories(Base):
    __tablename__='product_categories'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    category_name: Mapped[str]