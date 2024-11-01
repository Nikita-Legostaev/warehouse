from sqlalchemy import Integer, String, Date, ForeignKey
from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Product_features(Base):
    __tablename__='product_features'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    feature_description: Mapped[str]