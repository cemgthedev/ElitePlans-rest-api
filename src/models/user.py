from datetime import datetime
from pydantic import BaseModel, Field
from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from models.plan import Plan

class User(BaseModel):
    id: Optional[str] = Field(alias="_id")
    name: str = Field(alias="nome do usuário", min_length=3, max_length=120)
    email: str = Field(alias="email do usuário", min_length=3, max_length=80)
    password: str = Field(alias="senha do usuário", min_length=8, max_length=16)
    cpf: str = Field(alias="cpf", min_length=11, max_length=11)
    purchased_plans: Optional[List['Plan']] = Field(alias="planos comprados pelo usuário", default=[])
    created_plans: Optional[List['Plan']] = Field(alias="planos criados pelo usuário", default=[])
    created_at: datetime = Field(alias="data de criação", default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(alias="data da última atualização")