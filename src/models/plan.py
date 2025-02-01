from datetime import datetime
from pydantic import BaseModel, Field
from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from models.user import User
    from models.workout import Workout

class Plan(BaseModel):
    id: Optional[str] = Field(alias="_id")
    title: str = Field(alias="título do plano", min_length=3, max_length=120)
    description: str = Field(alias="descrição do plano")
    type: str = Field(alias="tipo de plano")
    category: str = Field(alias="categoria do plano")
    price: float = Field(alias="preço do plano")
    users: Optional[List['User']] = Field(alias="ids de usuários que possuem o plano", default=[])
    workouts: Optional[List['Workout']] = Field(alias="ids de treinos do plano", default=[])
    created_at: datetime = Field(alias="data de criação", default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(alias="data da última atualização")