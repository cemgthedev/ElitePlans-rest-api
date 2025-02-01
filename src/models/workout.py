from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

class Workout(BaseModel):
    id: Optional[str] = Field(alias="_id")
    title: str = Field(min_length=3, max_length=120)
    description: str = Field(min_length=3)
    rest_time: int = Field(min_length=0)
    type: str
    category: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default=None)