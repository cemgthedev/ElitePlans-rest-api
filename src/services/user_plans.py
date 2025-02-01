from fastapi import APIRouter
from database import db
from models.user_plans import UserPlans

# Criar roteador
router = APIRouter()