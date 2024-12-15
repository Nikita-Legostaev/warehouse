from app.repositories.base import BaseRepositories
from app.models.product_feature_association.models import Product_feature_association


class Product_feature_associationRepositories(BaseRepositories):
    model = Product_feature_association