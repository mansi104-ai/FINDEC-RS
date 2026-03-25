from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class RecommendationSchema(BaseModel):
    id: Optional[int] = None
    user_id: int
    title: str
    description: str
    category: str
    confidence: float
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
