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
        response = await db.users.insert_one(user_dict)
        
        created_user = await db.users.find_one({"_id": response.inserted_id})
        if not created_user:
            raise HTTPException(status_code=500, detail='Erro ao criar usuário')
        
        created_user["_id"] = str(created_user["_id"])
        users_logger.info(f'Usuário criado com sucesso: {created_user}')
        return created_user
    
    except Exception as e:
        users_logger.error(f'Erro ao criar usuário: {e}')
        raise HTTPException(status_code=500, detail='Erro ao criar usuário')
    
# Rota de atualização de um usuário
@router.put('/users/{id}')
async def update_user(id: str, user: User):
    try:
        users_logger.info(f'Atualizando usuário: {user}')
        user_dict = user.dict(by_alias=True, exclude={"id"})
        response = await db.users.update_one({"_id": ObjectId(id)}, {"$set": user_dict})
        
        if response.matched_count == 0:
            users_logger.warning(f'Usuário não encontrado: {id}')
            raise HTTPException(status_code=404, detail='Usuário não encontrado')
        
        if response.modified_count == 0:
            users_logger.warning(f'Nenhuma alteração foi feita no usuário: {user}')
            raise HTTPException(status_code=500, detail='Nenhuma alteração foi feita no usuário')
        
        updated_user = await db.users.find_one({"_id": ObjectId(id)})
        updated_user["_id"] = str(updated_user["_id"])
        users_logger.info(f'Usuário atualizado com sucesso: {updated_user}')
        return updated_user
    
    except Exception as e:
        users_logger.error(f'Erro ao atualizar usuário: {e}')
        raise HTTPException(status_code=500, detail='Erro ao atualizar usuário')
    
# Rota de exclusão de um usuário
@router.delete('/users/{id}')
async def delete_user(id: str):
    try:
        users_logger.info(f'Excluindo usuário: {id}')
        await db.user_plans.delete_many({"user_id": ObjectId(id)})
        response = await db.users.delete_one({"_id": ObjectId(id)})
        
        if response.deleted_count == 0:
            users_logger.warning(f'Usuário não encontrado: {id}')
            raise HTTPException(status_code=404, detail='Usuário não encontrado')
        
        users_logger.info(f'Usuário excluído com sucesso: {id}')
        return {"message": "Usuário excluído com sucesso"}
    
    except Exception as e:
        users_logger.error(f'Erro ao excluir usuário: {e}')
        raise HTTPException(status_code=500, detail='Erro ao excluir usuário')
    
# Rota de busca de um usuário por id
@router.get('/users/{id}')
async def get_user(id: str):
    try:
        users_logger.info(f'Buscando usuário: {id}')
        user = await db.users.find_one({"_id": ObjectId(id)})
        
        if not user:
            users_logger.warning(f'Usuário não encontrado: {id}')
            raise HTTPException(status_code=404, detail='Usuário não encontrado')
        
        user["_id"] = str(user["_id"])
        users_logger.info(f'Usuário encontrado: {user}')
        return user
    
    except Exception as e:
        users_logger.error(f'Erro ao buscar usuário: {e}')
        raise HTTPException(status_code=500, detail='Erro ao buscar usuário')