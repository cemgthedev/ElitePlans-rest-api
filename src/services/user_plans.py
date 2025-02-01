from fastapi import APIRouter
from database import db
from models.user_plans import UserPlans
from services.configs import user_plans_logger

# Criar roteador
router = APIRouter()