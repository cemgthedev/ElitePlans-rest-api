from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

class PlanWorkouts(BaseModel):
    id: Optional[str] = Field(alias="_id")
    plan_id: str = Field(alias="id do plano")
    workout_id: str = Field(alias="id do treino")
    created_at: datetime = Field(alias="data de criação", default_factory=datetime.now)