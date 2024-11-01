from app.repositories.base import BaseRepositories
from app.models.products.models import Products


class ProductsRepositories(BaseRepositories):
    model = Products 