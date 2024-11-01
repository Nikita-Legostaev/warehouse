from app.repositories.base import BaseRepositories
from app.models.product_categories.models import Product_categories


class CategoryRepositories(BaseRepositories):
    model = Product_categories 