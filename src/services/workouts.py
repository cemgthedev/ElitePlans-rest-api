from fastapi import APIRouter
from database import db
from models.workout import Workout

# Criar roteador
router = APIRouter()