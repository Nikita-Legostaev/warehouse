from pydantic import BaseModel
from datetime import date

class SPorducts(BaseModel):
    product_name: str
    manufacturer_id: int 
    category_id: int 
    price: int
    expiration_date: date 
    weight: int
    stock_id: int 
    stock_location: int
    stock_quantity: int 