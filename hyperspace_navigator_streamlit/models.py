from pydantic import BaseModel, validator
from typing import Optional

# Or Planet
class System(BaseModel):
    name: str
    x: float
    y: float
    region: str
    type: str = 'System'
    importance: Optional[float] = 0.0
    pagerank : Optional[float] = 0.0
    centrality : Optional[float] = 0.0
    affiliation: Optional[str] = "Unknown"


    @validator('importance', pre=True)
    def set_importance_default(cls, v):
        return float(v or 0.0)

