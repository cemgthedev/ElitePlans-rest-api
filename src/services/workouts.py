from typing import Literal, Optional
from bson import ObjectId
from fastapi import APIRouter, HTTPException, Query
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
    
# Rota de busca de um treino por id
@router.get('/workouts/{id}')
async def get_workout(id: str):
    try:
        workouts_logger.info(f'Buscando treino: {id}')
        workout = await db.workouts.find_one({"_id": ObjectId(id)})

        if not workout:
            workouts_logger.warning(f'Treino não encontrado: {id}')
            raise HTTPException(status_code=404, detail='Treino não encontrado')

        workout["_id"] = str(workout["_id"])
        workouts_logger.info(f'Treino encontrado: {workout}')
        return workout

    except Exception as e:
        workouts_logger.error(f'Erro ao buscar treino: {e}')
        raise HTTPException(status_code=500, detail='Erro ao buscar treino')

# Rota de listagem de treinos
@router.get('/workouts')
async def get_workouts(
    page: Optional[int] = Query(1, ge=1, description="Page number, starting from 1"),
    limit: Optional[int] = Query(10, ge=1, le=100, description="Number of results per page (max 100)"),
    sort_by: Optional[Literal["title", "type", "category", "rest_time"]] = Query(None, description="Sort by field"),
    order_by: Optional[Literal["asc", "desc"]] = Query(None, description="Order by field"),
    subject: Optional[str] = Query(None, min_length=3, max_length=120, description="Filter by subject"),
    type: Optional[str] = Query(None, min_length=3, max_length=120, description="Filter by type"),
    category: Optional[str] = Query(None, min_length=3, max_length=120, description="Filter by category"),
    min_rest_time: Optional[float] = Query(None, ge=0, description="Filter by minimum rest time"),
    max_rest_time: Optional[float] = Query(None, ge=0, description="Filter by maximum rest time")
):
    try:
        workouts_logger.info(f'Buscando treinos')
        filters = []
        
        if subject:
            filters.append({"$or": [{"title": {"$regex": subject, "$options": "i"}}, {"description": {"$regex": subject, "$options": "i"}}]})
        
        if type:
            filters.append({"type": type})
        
        if category:
            filters.append({"category": category})
        
        if min_rest_time:
            filters.append({"rest_time": {"$gte": min_rest_time}})
        
        if max_rest_time:
            filters.append({"rest_time": {"$lte": max_rest_time}})
        
        query = {"$and": filters} if filters else {}
        
        skip = (page - 1) * limit
        
        order_direction = None
        if order_by == "asc":
            order_direction = 1
        elif order_by == "desc":
            order_direction = -1
        
        workouts = []
        if sort_by and order_direction:
            workouts = await db.workouts.find(query).sort(sort_by, order_direction).skip(skip).limit(limit).to_list(length=limit)
        else:
            workouts = await db.workouts.find(query).skip(skip).limit(limit).to_list(length=limit)
        
        for workout in workouts:
            workout["_id"] = str(workout["_id"])
        
        if len(workouts) > 0:
            workouts_logger.info(f'Treinos encontrados com sucesso: {workouts}')
            return workouts
        else:
            workouts_logger.warning(f'Nenhum treino encontrado')
            raise HTTPException(status_code=404, detail='Nenhum treino encontrado')
    
    except Exception as e:
        workouts_logger.error(f'Erro ao buscar treinos: {e}')
        raise HTTPException(status_code=500, detail='Erro ao buscar treinos')
    
# Rota de quantidade de treinos
@router.get('/quantity/workouts')
async def get_workouts_quantity():
    try:
        workouts_logger.info(f'Buscando quantidade de treinos')
        quantity = await db.workouts.count_documents({})

        workouts_logger.info(f'Quantidade de treinos encontrada com sucesso: {quantity}')
        return {"quantity": quantity}

    except Exception as e:
        workouts_logger.error(f'Erro ao buscar quantidade de treinos: {e}')
        raise HTTPException(status_code=500, detail='Erro ao buscar quantidade de treinos')