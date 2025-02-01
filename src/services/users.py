from fastapi import APIRouter, HTTPException
from database import db
from models.user import User
from services.configs import users_logger

# Criar roteador
router = APIRouter()

# Rota de criação de um novo usuário
@router.post('/users')
async def create_user(user: User):
    try:
        users_logger.info(f'Criando usuário com id: {user.id}')
        user_dict = user.dict(by_alias=True, exclude={"id"})
        new_user = await db.users.insert_one(user_dict)
        
        created_user = await db.users.find_one({"_id": new_user.inserted_id})
        if not created_user:
            raise HTTPException(status_code=500, detail='Erro ao criar usuário')
        
        created_user["_id"] = str(created_user["_id"])
        return created_user
    
    except Exception as e:
        users_logger.error(f'Erro ao criar usuário: {e}')
        raise HTTPException(status_code=500, detail='Erro ao criar usuário')
    