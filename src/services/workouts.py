from fastapi import APIRouter
from database import db
from models.workout import Workout
from services.configs import workouts_logger

# Criar roteador
router = APIRouter()