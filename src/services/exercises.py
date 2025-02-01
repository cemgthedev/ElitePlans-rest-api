from fastapi import APIRouter
from database import db
from models.exercise import Exercise
from services.configs import exercises_logger

# Criar roteador
router = APIRouter()