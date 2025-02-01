from __future__ import annotations
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

class PlanWorkouts(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    plan_id: str
    workout_id: str
    created_at: datetime = Field(default_factory=datetime.now)