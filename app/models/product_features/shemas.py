from pydantic import BaseModel, ConfigDict

class SProductFeature(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    feature_description: str
    