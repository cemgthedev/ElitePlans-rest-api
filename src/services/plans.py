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
        new_plan = await db.plans.insert_one(plan_dict)
        
        created_plan = await db.plans.find_one({"_id": new_plan.inserted_id})
        if not created_plan:
            raise HTTPException(status_code=500, detail='Erro ao criar plano')
        
        created_plan["_id"] = str(created_plan["_id"])
        plans_logger.info(f'Plano criado com sucesso: {created_plan}')
        return created_plan
    
    except Exception as e:
        plans_logger.error(f'Erro ao criar plano: {e}')
        raise HTTPException(status_code=500, detail='Erro ao criar plano')
    
# Rota de atualização de um plano
@router.put('/plans/{plan_id}')
async def update_plan(plan_id: str, plan: Plan):
    try:
        plans_logger.info(f'Atualizando plano: {plan}')
        
        seller = await db.users.find_one({"_id": ObjectId(plan.seller_id)})
        if not seller:
            plans_logger.warning(f'Vendedor não encontrado: {plan.seller_id}')
            raise HTTPException(status_code=404, detail='Vendedor não encontrado')
        
        plan_dict = plan.dict(by_alias=True, exclude={"id"})
        updated_plan = await db.plans.update_one({"_id": ObjectId(plan_id)}, {"$set": plan_dict})
        
        if updated_plan.matched_count == 0:
            raise HTTPException(status_code=404, detail='Plano não encontrado')
        
        updated_plan = await db.plans.find_one({"_id": ObjectId(plan_id)})
        updated_plan["_id"] = str(updated_plan["_id"])
        plans_logger.info(f'Plano atualizado com sucesso: {updated_plan}')
        return updated_plan
    
    except Exception as e:
        plans_logger.error(f'Erro ao atualizar plano: {e}')
        raise HTTPException(status_code=500, detail='Erro ao atualizar plano')