from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

class Address(BaseModel):
    cep: Optional[str] = Field(min_length=8, max_length=8)
    street: str = Field(min_length=3, max_length=120)
    number: str = Field(min_length=1, max_length=10)
    neighborhood: str = Field(min_length=3, max_length=120)
    city: str = Field(min_length=3, max_length=120)
    state: Optional[str] = Field(min_length=2, max_length=2)

class User(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    name: str = Field(min_length=3, max_length=120)
    email: str = Field(min_length=3, max_length=80)
    password: str = Field(min_length=8, max_length=16)
    cpf: str = Field(min_length=11, max_length=11)
    phone_number: str
    address: Address
    plans_sold: Optional[list[str]] = []
    purchased_plans: Optional[list[str]] = []
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default=None)