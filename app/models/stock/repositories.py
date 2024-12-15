from app.repositories.base import BaseRepositories
from app.models.stock.models import Stock


class StockRepositories(BaseRepositories):
    model = Stock 