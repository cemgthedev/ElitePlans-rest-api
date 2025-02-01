from bson import ObjectId
from fastapi import APIRouter, HTTPException
from database import db
from models.plan import Plan
from services.configs import plans_logger

# Criar roteador
router = APIRouter()

# Rota de criação de um novo plano
@router.post('/plans')
async def create_plan(plan: Plan):
    try:
        plans_logger.info(f'Criando plano: {plan}')
        
        seller = await db.users.find_one({"_id": ObjectId(plan.seller_id)})
        if not seller:
            plans_logger.warning(f'Vendedor não encontrado: {plan.seller_id}')
            raise HTTPException(status_code=404, detail='Vendedor não encontrado')
        
        plan_dict = plan.dict(by_alias=True, exclude={"id"})
        response = await db.plans.insert_one(plan_dict)
        
        created_plan = await db.plans.find_one({"_id": response.inserted_id})
        if not created_plan:
            plans_logger.error(f'Erro ao criar plano: {plan}')
            raise HTTPException(status_code=500, detail='Erro ao criar plano')
        
        created_plan["_id"] = str(created_plan["_id"])
        plans_logger.info(f'Plano criado com sucesso: {created_plan}')
        return created_plan
    
    except Exception as e:
        plans_logger.error(f'Erro ao criar plano: {e}')
        raise HTTPException(status_code=500, detail='Erro ao criar plano')
    
# Rota de atualização de um plano
@router.put('/plans/{id}')
async def update_plan(id: str, plan: Plan):
    try:
        plans_logger.info(f'Atualizando plano: {plan}')
        
        seller = await db.users.find_one({"_id": ObjectId(plan.seller_id)})
        if not seller:
            plans_logger.warning(f'Vendedor não encontrado: {plan.seller_id}')
            raise HTTPException(status_code=404, detail='Vendedor não encontrado')
        
        plan_dict = plan.dict(by_alias=True, exclude={"id"})
        response = await db.plans.update_one({"_id": ObjectId(id)}, {"$set": plan_dict})
        
        if response.matched_count == 0:
            plans_logger.warning(f'Plano não encontrado: {id}')
            raise HTTPException(status_code=404, detail='Plano não encontrado')
        
        if response.modified_count == 0:
            plans_logger.warning(f'Nenhuma alteração foi feita no plano: {plan}')
            raise HTTPException(status_code=500, detail='Nenhuma alteração foi feita no plano')
        
        updated_plan = await db.plans.find_one({"_id": ObjectId(id)})
        updated_plan["_id"] = str(updated_plan["_id"])
        plans_logger.info(f'Plano atualizado com sucesso: {updated_plan}')
        return updated_plan
    
    except Exception as e:
        plans_logger.error(f'Erro ao atualizar plano: {e}')
        raise HTTPException(status_code=500, detail='Erro ao atualizar plano')
    
# Rota de exclusão de um plano
@router.delete('/plans/{id}')
async def delete_plan(id: str):
    try:
        plans_logger.info(f'Excluindo plano: {id}')
        await db.user_plans.delete_many({"plan_id": ObjectId(id)})
        response = await db.plans.delete_one({"_id": ObjectId(id)})
        
        if response.deleted_count == 0:
            plans_logger.warning(f'Plano não encontrado: {id}')
            raise HTTPException(status_code=404, detail='Plano não encontrado')
        
        plans_logger.info(f'Plano excluído com sucesso: {id}')
        return {"message": "Plano excluído com sucesso"}
    
    except Exception as e:
        plans_logger.error(f'Erro ao excluir plano: {e}')
        raise HTTPException(status_code=500, detail='Erro ao excluir plano')
    
# Rota de busca de um plano por id
@router.get('/plans/{id}')
async def get_plan(id: str):
    try:
        plans_logger.info(f'Buscando plano: {id}')
        plan = await db.plans.find_one({"_id": ObjectId(id)})
        
        if not plan:
            plans_logger.warning(f'Plano não encontrado: {id}')
            raise HTTPException(status_code=404, detail='Plano não encontrado')
        
        plan["_id"] = str(plan["_id"])
        plans_logger.info(f'Plano encontrado: {plan}')
        return plan
    
    except Exception as e:
        plans_logger.error(f'Erro ao buscar plano: {e}')
        raise HTTPException(status_code=500, detail='Erro ao buscar plano')
    
# Rota de quantidade de planos
@router.get('/quantity/plans')
async def get_plans_quantity():
    try:
        plans_logger.info(f'Buscando quantidade de planos')
        quantity = await db.plans.count_documents({})

        plans_logger.info(f'Quantidade de planos encontrada com sucesso: {quantity}')
        return {"quantity": quantity}

    except Exception as e:
        plans_logger.error(f'Erro ao buscar quantidade de planos: {e}')
        raise HTTPException(status_code=500, detail='Erro ao buscar quantidade de planos')