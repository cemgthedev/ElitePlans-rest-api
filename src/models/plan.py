from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

class Plan(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    title: str = Field(min_length=3, max_length=120)
    description: str = Field(min_length=3)
    type: str = Field(min_length=3)
    category: str = Field(min_length=3)
    price: float
    seller_id: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default=None)