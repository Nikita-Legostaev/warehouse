from pydantic import BaseModel

class SStock(BaseModel):
    row: int
    cell: int 