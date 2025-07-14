from pydantic import BaseModel
from typing import Optional

class AnalyzeRequest(BaseModel):
    pet_name: str
    breed: str
    weight: float
    symptoms: Optional[str] = None
    # image will be handled in Phase 2

class AnalyzeResponse(BaseModel):
    diagnosis: str
    advice: str 