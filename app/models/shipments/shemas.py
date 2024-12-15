from pydantic import BaseModel
from datetime import date

class SShipments(BaseModel):
    product_id: int 
    shipment_date: date 
    quantity: int
    supplier_name: str 