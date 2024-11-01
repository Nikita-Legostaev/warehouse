from app.repositories.base import BaseRepositories
from app.models.manufacturers.models import Manufacturers

class ManufacturersRepositories(BaseRepositories):
    model = Manufacturers