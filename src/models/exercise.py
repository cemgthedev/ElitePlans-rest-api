from __future__ import annotations
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

class Exercise(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    title: str = Field(min_length=3, max_length=120)
    n_sections: int = Field(ge=0)
    n_reps: int = Field(ge=0)
    weight: float = Field(ge=0)
    tutorial_url: Optional[str] = Field(default=None)
    workout_id: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default=None)