from bson import ObjectId
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
        users_logger.info(f'Criando usuário: {user}')
        user_dict = user.dict(by_alias=True, exclude={"id"})
        new_user = await db.users.insert_one(user_dict)
        
        created_user = await db.users.find_one({"_id": new_user.inserted_id})
        if not created_user:
            raise HTTPException(status_code=500, detail='Erro ao criar usuário')
        
        created_user["_id"] = str(created_user["_id"])
        users_logger.info(f'Usuário criado com sucesso: {created_user}')
        return created_user
    
    except Exception as e:
        users_logger.error(f'Erro ao criar usuário: {e}')
        raise HTTPException(status_code=500, detail='Erro ao criar usuário')
    
# Rota de atualização de um usuário
@router.put('/users/{user_id}')
async def update_user(user_id: str, user: User):
    try:
        users_logger.info(f'Atualizando usuário: {user}')
        user_dict = user.dict(by_alias=True, exclude={"id"})
        updated_user = await db.users.update_one({"_id": ObjectId(user_id)}, {"$set": user_dict})
        
        if updated_user.matched_count == 0:
            raise HTTPException(status_code=404, detail='Usuário não encontrado')
        
        updated_user = await db.users.find_one({"_id": ObjectId(user_id)})
        updated_user["_id"] = str(updated_user["_id"])
        users_logger.info(f'Usuário atualizado com sucesso: {updated_user}')
        return updated_user
    
    except Exception as e:
        users_logger.error(f'Erro ao atualizar usuário: {e}')
        raise HTTPException(status_code=500, detail='Erro ao atualizar usuário')
    