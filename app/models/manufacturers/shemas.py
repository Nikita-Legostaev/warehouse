from pydantic import BaseModel, ConfigDict

class SManufact(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    manufacturer_name: str
    address: str
    email: str
