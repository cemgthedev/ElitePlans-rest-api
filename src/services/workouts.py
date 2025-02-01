from fastapi import APIRouter, HTTPException
from database import db
from models.workout import Workout
from services.configs import workouts_logger

# Criar roteador
router = APIRouter()

# Rota de criação de um novo treino
@router.post('/workouts')
async def create_workout(workout: Workout):
    try:
        workouts_logger.info(f'Criando treino: {workout}')
        workout_dict = workout.dict(by_alias=True, exclude={"id"})
        new_workout = await db.workouts.insert_one(workout_dict)

        created_workout = await db.workouts.find_one({"_id": new_workout.inserted_id})
        if not created_workout:
            raise HTTPException(status_code=500, detail='Erro ao criar treino')

        created_workout["_id"] = str(created_workout["_id"])
        workouts_logger.info(f'Treino criado com sucesso: {created_workout}')
        return created_workout

    except Exception as e:
        workouts_logger.error(f'Erro ao criar treino: {e}')
        raise HTTPException(status_code=500, detail='Erro ao criar treino')