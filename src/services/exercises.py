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
@router.put('/exercises/{id}')
async def update_exercise(id: str, exercise: Exercise):
    try:
        exercises_logger.info(f'Atualizando exercício: {exercise}')
        workout = await db.workouts.find_one({"_id": ObjectId(exercise.workout_id)})
        if not workout:
            exercises_logger.warning(f'Treino não encontrado: {exercise.workout_id}')
            raise HTTPException(status_code=404, detail='Treino não encontrado')
        
        exercise_dict = exercise.dict(by_alias=True, exclude={"id"})
        response = await db.exercises.update_one({"_id": ObjectId(id)}, {"$set": exercise_dict})

        if response.matched_count == 0:
            exercises_logger.warning(f'Exercício não encontrado: {id}')
            raise HTTPException(status_code=404, detail='Exercício não encontrado')
        
        if response.modified_count == 0:
            exercises_logger.warning(f'Nenhuma alteração foi feita no exercício: {exercise}')
            raise HTTPException(status_code=500, detail='Nenhuma alteração foi feita no exercício')

        updated_exercise = await db.exercises.find_one({"_id": ObjectId(id)})
        updated_exercise["_id"] = str(updated_exercise["_id"])
        exercises_logger.info(f'Exercício atualizado com sucesso: {updated_exercise}')
        return updated_exercise

    except Exception as e:
        exercises_logger.error(f'Erro ao atualizar exercício: {e}')
        raise HTTPException(status_code=500, detail='Erro ao atualizar exercício')
    
# Rota de exclusão de um exercício
@router.delete('/exercises/{id}')
async def delete_exercise(id: str):
    try:
        exercises_logger.info(f'Excluindo exercício: {id}')
        response = await db.exercises.delete_one({"_id": ObjectId(id)})

        if response.deleted_count == 0:
            exercises_logger.warning(f'Exercício não encontrado: {id}')
            raise HTTPException(status_code=404, detail='Exercício não encontrado')
        
        exercises_logger.info(f'Exercício excluído com sucesso: {id}')
        return {"message": "Exercício excluído com sucesso"}

    except Exception as e:
        exercises_logger.error(f'Erro ao excluir exercício: {e}')
        raise HTTPException(status_code=500, detail='Erro ao excluir exercício')
    
# Rota de busca de um exercício por id
@router.get('/exercises/{id}')
async def get_exercise(id: str):
    try:
        exercises_logger.info(f'Buscando exercício: {id}')
        exercise = await db.exercises.find_one({"_id": ObjectId(id)})

        if not exercise:
            exercises_logger.warning(f'Exercício não encontrado: {id}')
            raise HTTPException(status_code=404, detail='Exercício não encontrado')
        
        exercise["_id"] = str(exercise["_id"])
        exercises_logger.info(f'Exercício encontrado com sucesso: {exercise}')
        return exercise

    except Exception as e:
        exercises_logger.error(f'Erro ao buscar exercício: {e}')
        raise HTTPException(status_code=500, detail='Erro ao buscar exercício')
    
# Rota de quantidade de exercícios
@router.get('/quantity/exercises')
async def get_exercises_quantity():
    try:
        exercises_logger.info(f'Buscando quantidade de exercícios')
        quantity = await db.exercises.count_documents({})

        exercises_logger.info(f'Quantidade de exercícios encontrada com sucesso: {quantity}')
        return {"quantity": quantity}

    except Exception as e:
        exercises_logger.error(f'Erro ao buscar quantidade de exercícios: {e}')
        raise HTTPException(status_code=500, detail='Erro ao buscar quantidade de exercícios')
    
# Rota de quantidade de exercícios por treino
@router.get('/quantity/exercises/{id}')
async def get_exercises_quantity_by_workout(id: str):
    try:
        exercises_logger.info(f'Buscando quantidade de exercícios por treino: {id}')
        quantity = await db.exercises.count_documents({"workout_id": id})

        exercises_logger.info(f'Quantidade de exercícios por treino encontrada com sucesso: {quantity}')
        return {"quantity": quantity}

    except Exception as e:
        exercises_logger.error(f'Erro ao buscar quantidade de exercícios por treino: {e}')
        raise HTTPException(status_code=500, detail='Erro ao buscar quantidade de exercícios por treino')