from bson import ObjectId
from fastapi import APIRouter, HTTPException
from database import db
from models.user_plans import UserPlans
from services.configs import user_plans_logger

# Criar roteador
router = APIRouter()

# Rota de criação de um plano de treino para um usuário
@router.post('/user_plans')
async def create_user_plan(user_plan: UserPlans):
    try:
        user_plans_logger.info(f'Criando plano de treino para usuário: {user_plan}')
        
        seller = await db.users.find_one({"_id": ObjectId(user_plan.seller_id)})
        if not seller:
            user_plans_logger.warning(f'Vendedor não encontrado: {user_plan.seller_id}')
            raise HTTPException(status_code=404, detail='Vendedor não encontrado')
        
        buyer = await db.users.find_one({"_id": ObjectId(user_plan.buyer_id)})
        if not buyer:
            user_plans_logger.warning(f'Comprador não encontrado: {user_plan.buyer_id}')
            raise HTTPException(status_code=404, detail='Comprador não encontrado')
        
        plan = await db.plans.find_one({"_id": ObjectId(user_plan.plan_id)})
        if not plan:
            user_plans_logger.warning(f'Plano não encontrado: {user_plan.plan_id}')
            raise HTTPException(status_code=404, detail='Plano não encontrado')
        
        user_plan_dict = user_plan.dict(by_alias=True, exclude={"id"})
        new_user_plan = await db.user_plans.insert_one(user_plan_dict)

        created_user_plan = await db.user_plans.find_one({"_id": new_user_plan.inserted_id})
        if not created_user_plan:
            raise HTTPException(status_code=500, detail='Erro ao criar plano de treino para usuário')

        created_user_plan["_id"] = str(created_user_plan["_id"])
        user_plans_logger.info(f'Plano de treino para usuário criado com sucesso: {created_user_plan}')
        return created_user_plan

    except Exception as e:
        user_plans_logger.error(f'Erro ao criar plano de treino para usuário: {e}')
        raise HTTPException(status_code=500, detail='Erro ao criar plano de treino para usuário')