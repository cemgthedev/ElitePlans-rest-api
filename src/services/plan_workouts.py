from fastapi import APIRouter
from database import db
from models.plan_workouts import PlanWorkouts
from services.configs import plan_workouts_logger

# Criar roteador
router = APIRouter()