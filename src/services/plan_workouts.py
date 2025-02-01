from fastapi import APIRouter
from database import db
from models.plan_workouts import PlanWorkouts

# Criar roteador
router = APIRouter()