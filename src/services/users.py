from typing import Literal, Optional
from bson import ObjectId
from fastapi import APIRouter, HTTPException, Query
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
        response = await db.users.find_one({"email": user.email})
        if response:
            users_logger.warning(f'Usuário com email {user.email} já cadastrado')
            raise HTTPException(status_code=409, detail='Usuário com email já cadastrado')
        
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
    
# Rota de listagem de usuários
@router.get('/users')
async def get_users(
    page: Optional[int] = Query(1, ge=1, description="Page number, starting from 1"),
    limit: Optional[int] = Query(10, ge=1, le=100, description="Number of results per page (max 100)"),
    sort_by: Optional[Literal["name"]] = Query(None, description="Sort by field"),
    order_by: Optional[Literal["asc", "desc"]] = Query(None, description="Order by field"),
    name: Optional[str] = Query(None, min_length=3, max_length=120, description="Filter by name"),
    email: Optional[str] = Query(None, min_length=3, max_length=80, description="Filter by email"),
    password: Optional[str] = Query(None, min_length=8, max_length=16, description="Filter by password"),
):
    try:
        users_logger.info(f'Buscando usuários')
        filters = []
        
        if name:
            filters.append({"$text": {"$search": name}})
        
        if email and password:
            filters.append({"email": email, "password": password})

        query = {"$and": filters} if filters else {}
        
        skip = (page - 1) * limit
        
        order_direction = None
        if sort_by and order_by == "asc":
            order_direction = 1
        elif sort_by and order_by == "desc":
            order_direction = -1
        
        users = []
        if sort_by and order_direction:
            users = await db.users.find(query).sort(sort_by, order_direction).skip(skip).limit(limit).to_list(length=limit)
        else:
            users = await db.users.find(query).skip(skip).limit(limit).to_list(length=limit)
        
        for user in users:
            user["_id"] = str(user["_id"])
            user["plans_sold"] = [str(plan_id) for plan_id in user["plans_sold"]]
            user["purchased_plans"] = [str(plan_id) for plan_id in user["purchased_plans"]]
        
        if len(users) > 0:
            users_logger.info(f'Usuários encontrados com sucesso: {users}')
            return users
        else:
            users_logger.warning(f'Nenhum usuário encontrado')
            raise HTTPException(status_code=404, detail='Nenhum usuário encontrado')
    
    except Exception as e:
        users_logger.error(f'Erro ao buscar usuários: {e}')
        raise HTTPException(status_code=500, detail='Erro ao buscar usuários')
    
# Rota de quantidade de usuários
@router.get('/quantity/users')
async def get_users_quantity():
    try:
        users_logger.info(f'Buscando quantidade de usuários')
        quantity = await db.users.count_documents({})

        users_logger.info(f'Quantidade de usuários encontrada com sucesso: {quantity}')
        return {"quantity": quantity}

    except Exception as e:
        users_logger.error(f'Erro ao buscar quantidade de usuários: {e}')
        raise HTTPException(status_code=500, detail='Erro ao buscar quantidade de usuários')
    
# Rota de listagem dos planos de um vendedor
@router.get('/seller_plans/{id}')
async def get_seller_plans_by_id(id: str):
    try:
        users_logger.info(f'Buscando planos do vendedor')
        
        filters = []
        filters.append({"_id": ObjectId(id)})
        filters.append({ "plans_sold": { "$exists": True, "$ne": [] }})
        
        query = {"$and": filters}
        
        pipeline = [
            {"$match": query},
            {
                "$lookup": {
                    "from": "plans",
                    "localField": "plans_sold",
                    "foreignField": "_id",
                    "as": "plans_sold_details"
                }
            },
            {
                "$project": {"purchased_plans": 0}
            }
        ]
        
        user = await db.users.aggregate(pipeline).to_list(length=1)
            
        if user:
            user_dict = dict(user[0])
            user_dict["_id"] = str(user_dict["_id"])
            user_dict["plans_sold"] = [str(plan_id) for plan_id in user_dict["plans_sold"]]
            
            for plan in user_dict["plans_sold_details"]:
                plan["_id"] = str(plan["_id"])
            
            users_logger.info(f'Vendedor encontrado com sucesso: {user_dict}')
            return user_dict
        else:
            users_logger.warning(f'Nenhum vendedor encontrado')
            raise HTTPException(status_code=404, detail='Nenhum vendedor encontrado')

    except Exception as e:
        users_logger.error(f'Erro ao buscar planos do vendedor: {e}')
        raise HTTPException(status_code=500, detail='Erro ao buscar planos do vendedor')
    
# Rota de listagem dos planos dos vendedores
@router.get('/seller_plans')
async def get_seller_plans(
    page: Optional[int] = Query(1, ge=1, description="Page number, starting from 1"),
    limit: Optional[int] = Query(10, ge=1, le=100, description="Number of results per page (max 100)"),
    sort_by: Optional[Literal["name"]] = Query(None, description="Sort by field"),
    order_by: Optional[Literal["asc", "desc"]] = Query(None, description="Order by field"),
    name: Optional[str] = Query(None, min_length=3, max_length=120, description="Filter by name"),
    email: Optional[str] = Query(None, min_length=3, max_length=80, description="Filter by email"),
    password: Optional[str] = Query(None, min_length=8, max_length=16, description="Filter by password"),
):
    try:
        users_logger.info(f'Buscando planos dos vendedores')
        
        filters = []
        
        if name:
            filters.append({"$text": {"$search": name}})
        
        if email and password:
            filters.append({"email": email, "password": password})
            
        filters.append({ "plans_sold": { "$exists": True, "$ne": [] }})
        
        query = {"$and": filters}
        
        pipeline = [
            {"$match": query},
            {
                "$lookup": {
                    "from": "plans",
                    "localField": "plans_sold",
                    "foreignField": "_id",
                    "as": "plans_sold_details"
                }
            },
            {
                "$project": {"purchased_plans": 0}
            }
        ]
        
        skip = (page - 1) * limit
        pipeline.append({"$skip": skip})
        pipeline.append({"$limit": limit})
        
        order_direction = None
        if sort_by and order_by == "asc":
            order_direction = 1
        elif sort_by and order_by == "desc":
            order_direction = -1
        
        if sort_by and order_direction:
            pipeline.append({"$sort": {sort_by: order_direction}})
        
        users = await db.users.aggregate(pipeline).to_list(length=None)
        
        for user in users:
            user["_id"] = str(user["_id"])
            user["plans_sold"] = [str(plan_id) for plan_id in user["plans_sold"]]
            
            for plan in user["plans_sold_details"]:
                plan["_id"] = str(plan["_id"])
            
        if len(users) > 0:
            users_logger.info(f'Vendedores encontrados com sucesso: {users}')
            return users
        else:
            users_logger.warning(f'Nenhum vendedor encontrado')
            raise HTTPException(status_code=404, detail='Nenhum vendedor encontrado')

    except Exception as e:
        users_logger.error(f'Erro ao buscar planos dos vendedores: {e}')
        raise HTTPException(status_code=500, detail='Erro ao buscar planos dos vendedores')
    

# Rota de listagem dos planos de um comprador
@router.get('/buyer_plans/{id}')
async def get_buyer_plans_by_id(id: str):
    try:
        users_logger.info(f'Buscando planos do comprador')
        
        filters = []
        filters.append({"_id": ObjectId(id)})
        filters.append({ "purchased_plans": { "$exists": True, "$ne": [] }})
        
        query = {"$and": filters}
        
        pipeline = [
            {"$match": query},
            {
                "$lookup": {
                    "from": "plans",
                    "localField": "purchased_plans",
                    "foreignField": "_id",
                    "as": "purchased_plans_details"
                }
            },
            {
                "$project": {"plans_sold": 0}
            }
        ]
        
        user = await db.users.aggregate(pipeline).to_list(length=1)
            
        if user:
            user_dict = dict(user[0])
            user_dict["_id"] = str(user_dict["_id"])
            user_dict["purchased_plans"] = [str(plan_id) for plan_id in user_dict["purchased_plans"]]
            
            for plan in user_dict["purchased_plans_details"]:
                plan["_id"] = str(plan["_id"])
            
            users_logger.info(f'Comprador encontrado com sucesso: {user_dict}')
            return user_dict
        else:
            users_logger.warning(f'Nenhum comprador encontrado')
            raise HTTPException(status_code=404, detail='Nenhum comprador encontrado')

    except Exception as e:
        users_logger.error(f'Erro ao buscar planos do comprador: {e}')
        raise HTTPException(status_code=500, detail='Erro ao buscar planos do comprador')
    
# Rota de listagem dos planos dos compradores
@router.get('/buyer_plans')
async def get_buyer_plans(
    page: Optional[int] = Query(1, ge=1, description="Page number, starting from 1"),
    limit: Optional[int] = Query(10, ge=1, le=100, description="Number of results per page (max 100)"),
    sort_by: Optional[Literal["name"]] = Query(None, description="Sort by field"),
    order_by: Optional[Literal["asc", "desc"]] = Query(None, description="Order by field"),
    name: Optional[str] = Query(None, min_length=3, max_length=120, description="Filter by name"),
    email: Optional[str] = Query(None, min_length=3, max_length=80, description="Filter by email"),
    password: Optional[str] = Query(None, min_length=8, max_length=16, description="Filter by password"),
):
    try:
        users_logger.info(f'Buscando planos dos compradores')
        
        filters = []
        
        if name:
            filters.append({"$text": {"$search": name}})
        
        if email and password:
            filters.append({"email": email, "password": password})
            
        filters.append({ "purchased_plans": { "$exists": True, "$ne": [] }})
        
        query = {"$and": filters}
        
        pipeline = [
            {"$match": query},
            {
                "$lookup": {
                    "from": "plans",
                    "localField": "purchased_plans",
                    "foreignField": "_id",
                    "as": "purchased_plans_details"
                }
            },
            {
                "$project": {"plans_sold": 0}
            }
        ]
        
        skip = (page - 1) * limit
        pipeline.append({"$skip": skip})
        pipeline.append({"$limit": limit})
        
        order_direction = None
        if sort_by and order_by == "asc":
            order_direction = 1
        elif sort_by and order_by == "desc":
            order_direction = -1
        
        if sort_by and order_direction:
            pipeline.append({"$sort": {sort_by: order_direction}})
        
        users = await db.users.aggregate(pipeline).to_list(length=None)
        
        for user in users:
            user["_id"] = str(user["_id"])
            user["purchased_plans"] = [str(plan_id) for plan_id in user["purchased_plans"]]
            
            for plan in user["purchased_plans_details"]:
                plan["_id"] = str(plan["_id"])
            
        if len(users) > 0:
            users_logger.info(f'Compradores encontrados com sucesso: {users}')
            return users
        else:
            users_logger.warning(f'Nenhum comprador encontrado')
            raise HTTPException(status_code=404, detail='Nenhum comprador encontrado')

    except Exception as e:
        users_logger.error(f'Erro ao buscar planos dos compradores: {e}')
        raise HTTPException(status_code=500, detail='Erro ao buscar planos dos compradores')