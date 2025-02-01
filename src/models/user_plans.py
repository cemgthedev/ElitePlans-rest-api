from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

class UserPlans(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    seller_id: str
    buyer_id: str
    plan_id: str
    purchased: bool = Field(default=False)
    purchased_at: Optional[datetime] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.now)