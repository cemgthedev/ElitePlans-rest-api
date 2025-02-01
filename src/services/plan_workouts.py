from bson import ObjectId
from fastapi import APIRouter, HTTPException
from database import db
from models.plan_workouts import PlanWorkouts
from services.configs import plan_workouts_logger

# Criar roteador
router = APIRouter()

# Rota de criação de um novo treino do plano
@router.post('/plan_workouts')
async def create_plan_workout(plan_workout: PlanWorkouts):
    try:
        plan_workouts_logger.info(f'Criando treino do plano: {plan_workout}')
        
        plan = await db.plans.find_one({"_id": ObjectId(plan_workout.plan_id)})
        if not plan:
            plan_workouts_logger.warning(f'Plano não encontrado: {plan_workout.plan_id}')
            raise HTTPException(status_code=404, detail='Plano não encontrado')
        
        workout = await db.workouts.find_one({"_id": ObjectId(plan_workout.workout_id)})
        if not workout:
            plan_workouts_logger.warning(f'Treino não encontrado: {plan_workout.workout_id}')
            raise HTTPException(status_code=404, detail='Treino não encontrado')
        
        plan_workout_dict = plan_workout.dict(by_alias=True, exclude={"id"})
        response = await db.plan_workouts.insert_one(plan_workout_dict)

        created_plan_workout = await db.plan_workouts.find_one({"_id": response.inserted_id})
        if not created_plan_workout:
            plan_workouts_logger.error(f'Erro ao criar treino do plano: {plan_workout}')
            raise HTTPException(status_code=500, detail='Erro ao criar treino do plano')

        created_plan_workout["_id"] = str(created_plan_workout["_id"])
        plan_workouts_logger.info(f'Treino do plano criado com sucesso: {created_plan_workout}')
        return created_plan_workout

    except Exception as e:
        plan_workouts_logger.error(f'Erro ao criar treino do plano: {e}')
        raise HTTPException(status_code=500, detail='Erro ao criar treino do plano')
    
# Rota de remoção de treino de plano
@router.delete('/plan_workouts/{id}')
async def delete_plan_workout(id: str):
    try:
        plan_workouts_logger.info(f'Excluindo treino do plano: {id}')
        response = await db.plan_workouts.delete_one({"_id": ObjectId(id)})

        if response.deleted_count == 0:
            plan_workouts_logger.warning(f'Treino do plano não encontrado: {id}')
            raise HTTPException(status_code=404, detail='Treino do plano não encontrado')

        plan_workouts_logger.info(f'Treino do plano excluído com sucesso: {id}')
        return {"message": "Treino do plano excluído com sucesso"}

    except Exception as e:
        plan_workouts_logger.error(f'Erro ao excluir treino do plano: {e}')
        raise HTTPException(status_code=500, detail='Erro ao excluir treino do plano')