from app.repositories.base import BaseRepositories
from app.models.shipments.models import Shipments


class ShipmentsRepositories(BaseRepositories):
    model = Shipments 