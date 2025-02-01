from fastapi import APIRouter
from database import db
from models.plan import Plan
from services.configs import plans_logger

# Criar roteador
router = APIRouter()