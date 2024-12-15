from app.repositories.base import BaseRepositories
from app.models.product_features.models import Product_features


class Product_featuresRepositories(BaseRepositories):
    model = Product_features