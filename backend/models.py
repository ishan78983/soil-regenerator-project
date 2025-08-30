from pydantic import BaseModel, Field
from typing import Optional

class SoilDataInput(BaseModel):
    location: Optional[str] = Field(None, example="Indore, Madhya Pradesh")
    ph_level: float = Field(..., ge=0, le=14, example=6.5)
    organic_matter: float = Field(..., ge=0, le=100, example=3.2)
    moisture_content: float = Field(..., ge=0, le=100, example=25.0)
    previous_crop: Optional[str] = Field(None, example="Soybean")