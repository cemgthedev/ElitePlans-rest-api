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