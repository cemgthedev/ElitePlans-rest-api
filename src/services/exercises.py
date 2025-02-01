from bson import ObjectId
from fastapi import APIRouter, HTTPException
from database import db
from models.exercise import Exercise
from services.configs import exercises_logger

# Criar roteador
router = APIRouter()

# Rota de criação de um novo exercício
@router.post('/exercises')
async def create_exercise(exercise: Exercise):
    try:
        exercises_logger.info(f'Criando exercício: {exercise}')
        workout = await db.workouts.find_one({"_id": ObjectId(exercise.workout_id)})
        if not workout:
            exercises_logger.warning(f'Treino não encontrado: {exercise.workout_id}')
            raise HTTPException(status_code=404, detail='Treino não encontrado')
        
        exercise_dict = exercise.dict(by_alias=True, exclude={"id"})
        new_exercise = await db.exercises.insert_one(exercise_dict)

        created_exercise = await db.exercises.find_one({"_id": new_exercise.inserted_id})
        if not created_exercise:
            raise HTTPException(status_code=500, detail='Erro ao criar exercício')

        created_exercise["_id"] = str(created_exercise["_id"])
        exercises_logger.info(f'Exercício criado com sucesso: {created_exercise}')
        return created_exercise

    except Exception as e:
        exercises_logger.error(f'Erro ao criar exercício: {e}')
        raise HTTPException(status_code=500, detail='Erro ao criar exercício')
    
# Rota de atualização de um exercício
@router.put('/exercises/{exercise_id}')
async def update_exercise(exercise_id: str, exercise: Exercise):
    try:
        exercises_logger.info(f'Atualizando exercício: {exercise}')
        workout = await db.workouts.find_one({"_id": ObjectId(exercise.workout_id)})
        if not workout:
            exercises_logger.warning(f'Treino não encontrado: {exercise.workout_id}')
            raise HTTPException(status_code=404, detail='Treino não encontrado')
        
        exercise_dict = exercise.dict(by_alias=True, exclude={"id"})
        updated_exercise = await db.exercises.update_one({"_id": ObjectId(exercise_id)}, {"$set": exercise_dict})

        if updated_exercise.matched_count == 0:
            raise HTTPException(status_code=404, detail='Exercício não encontrado')

        updated_exercise = await db.exercises.find_one({"_id": ObjectId(exercise_id)})
        updated_exercise["_id"] = str(updated_exercise["_id"])
        exercises_logger.info(f'Exercício atualizado com sucesso: {updated_exercise}')
        return updated_exercise

    except Exception as e:
        exercises_logger.error(f'Erro ao atualizar exercício: {e}')
        raise HTTPException(status_code=500, detail='Erro ao atualizar exercício')