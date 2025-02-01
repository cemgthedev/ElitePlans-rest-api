from datetime import datetime
from pydantic import BaseModel, Field
from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from models.plan import Plan
    from models.exercise import Exercise

class Workout(BaseModel):
    id: Optional[str] = Field(alias="_id")
    title: str = Field(alias="título do treino", min_length=3, max_length=120)
    description: str = Field(alias="descrição do treino")
    rest_time: int = Field(alias="tempo de descanso em segundos")
    type: str = Field(alias="tipo de treino")
    category: str = Field(alias="categoria do treino")
    plans: Optional[List['Plan']] = Field(alias="planos que possuem o treino", default=[])
    exercises: Optional[List['Exercise']] = Field(alias="exercícios do treino", default=[])
    created_at: datetime = Field(alias="data de criação", default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(alias="data da última atualização")