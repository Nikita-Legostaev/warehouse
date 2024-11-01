from pydantic import BaseModel, ConfigDict

class SCategory(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    category_name: str