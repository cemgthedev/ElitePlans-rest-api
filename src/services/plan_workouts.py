from bson import ObjectId
from fastapi import APIRouter, HTTPException
from database import db
from models.plan_workouts import PlanWorkouts
from services.configs import plan_workouts_logger

# Criar roteador
router = APIRouter()

# Rota de criação de um novo plano de treino
@router.post('/plan_workouts')
async def create_plan_workout(plan_workout: PlanWorkouts):
    try:
        plan_workouts_logger.info(f'Criando plano de treino: {plan_workout}')
        
        plan = await db.plans.find_one({"_id": ObjectId(plan_workout.plan_id)})
        if not plan:
            raise HTTPException(status_code=404, detail='Plano não encontrado')
        
        workout = await db.workouts.find_one({"_id": ObjectId(plan_workout.workout_id)})
        if not workout:
            raise HTTPException(status_code=404, detail='Treino não encontrado')
        
        plan_workout_dict = plan_workout.dict(by_alias=True, exclude={"id"})
        new_plan_workout = await db.plan_workouts.insert_one(plan_workout_dict)

        created_plan_workout = await db.plan_workouts.find_one({"_id": new_plan_workout.inserted_id})
        if not created_plan_workout:
            raise HTTPException(status_code=500, detail='Erro ao criar plano de treino')

        created_plan_workout["_id"] = str(created_plan_workout["_id"])
        plan_workouts_logger.info(f'Plano de treino criado com sucesso: {created_plan_workout}')
        return created_plan_workout

    except Exception as e:
        plan_workouts_logger.error(f'Erro ao criar plano de treino: {e}')
        raise HTTPException(status_code=500, detail='Erro ao criar plano de treino')