from pydantic import BaseModel, validator
from typing import Optional

# Or Planet
class System(BaseModel):
    name: str
    X: float
    Y: float
    description: Optional[str] = None
    Region: Optional[str] = None
    type: Optional[str] = None
    importance: Optional[float] = 0.0
    Link: Optional[str] = None


    @validator('importance', pre=True)
    def set_importance_default(cls, v):
        return float(v or 0.0)

