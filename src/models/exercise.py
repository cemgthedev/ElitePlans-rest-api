from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

class Exercise(BaseModel):
    id: Optional[str] = Field(alias="_id")
    title: str = Field(alias="título do plano", min_length=3, max_length=120)
    n_sections: int = Field(alias="quantidade de seções")
    n_reps: int = Field(alias="quantidade de repetições por seção")
    weight: float = Field(alias="peso")
    tutorial_url: str = Field(alias="url do tutorial")
    workout_id: str = Field(alias="id do treino")
    created_at: datetime = Field(alias="data de criação", default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(alias="data da última atualização")