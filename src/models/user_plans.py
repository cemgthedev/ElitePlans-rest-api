from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

class UserPlans(BaseModel):
    id: Optional[str] = Field(alias="_id")
    user_id: str = Field(alias="id do usuário")
    plan_id: str = Field(alias="id do plano")
    created_at: datetime = Field(alias="data de criação", default_factory=datetime.now)