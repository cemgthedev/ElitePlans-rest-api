from bson import ObjectId
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
        response = await db.workouts.insert_one(workout_dict)

        created_workout = await db.workouts.find_one({"_id": response.inserted_id})
        if not created_workout:
            raise HTTPException(status_code=500, detail='Erro ao criar treino')

        created_workout["_id"] = str(created_workout["_id"])
        workouts_logger.info(f'Treino criado com sucesso: {created_workout}')
        return created_workout

    except Exception as e:
        workouts_logger.error(f'Erro ao criar treino: {e}')
        raise HTTPException(status_code=500, detail='Erro ao criar treino')
    
# Rota de atualização de um treino
@router.put('/workouts/{id}')
async def update_workout(id: str, workout: Workout):
    try:
        workouts_logger.info(f'Atualizando treino: {workout}')
        workout_dict = workout.dict(by_alias=True, exclude={"id"})
        response = await db.workouts.update_one({"_id": ObjectId(id)}, {"$set": workout_dict})

        if response.matched_count == 0:
            workouts_logger.warning(f'Treino não encontrado: {id}')
            raise HTTPException(status_code=404, detail='Treino não encontrado')
        
        if response.modified_count == 0:
            workouts_logger.warning(f'Nenhuma alteração foi feita no treino: {workout}')
            raise HTTPException(status_code=500, detail='Nenhuma alteração foi feita no treino')

        updated_workout = await db.workouts.find_one({"_id": ObjectId(id)})
        updated_workout["_id"] = str(updated_workout["_id"])
        workouts_logger.info(f'Treino atualizado com sucesso: {updated_workout}')
        return updated_workout

    except Exception as e:
        workouts_logger.error(f'Erro ao atualizar treino: {e}')
        raise HTTPException(status_code=500, detail='Erro ao atualizar treino')
    
# Rota de exclusão de um treino
@router.delete('/workouts/{id}')
async def delete_workout(id: str):
    try:
        workouts_logger.info(f'Excluindo treino: {id}')
        await db.exercises.delete_many({"workout_id": ObjectId(id)})
        response = await db.workouts.delete_one({"_id": ObjectId(id)})

        if response.deleted_count == 0:
            workouts_logger.warning(f'Treino não encontrado: {id}')
            raise HTTPException(status_code=404, detail='Treino não encontrado')
        
        workouts_logger.info(f'Treino excluído com sucesso: {id}')
        return {"message": "Treino excluído com sucesso"}

    except Exception as e:
        workouts_logger.error(f'Erro ao excluir treino: {e}')
        raise HTTPException(status_code=500, detail='Erro ao excluir treino')