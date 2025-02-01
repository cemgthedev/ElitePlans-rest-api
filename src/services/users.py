from fastapi import APIRouter
from database import db
from models.user import User
from services.configs import users_logger

# Criar roteador
router = APIRouter()