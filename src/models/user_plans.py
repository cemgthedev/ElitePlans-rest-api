from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

class UserPlans(BaseModel):
    id: Optional[str] = Field(alias="_id")
    seller_id: str = Field(alias="id do vendedor")
    buyer_id: str = Field(alias="id do comprador")
    plan_id: str = Field(alias="id do plano")
    purchased: bool = Field(alias="comprado", default=False)
    purchased_at: Optional[datetime] = Field(alias="data da compra", default=None)
    created_at: datetime = Field(alias="data de criação", default_factory=datetime.now)