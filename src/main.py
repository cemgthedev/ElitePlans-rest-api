from fastapi import FastAPI, Depends
from database import get_db
from services.users import router as users_router
from services.exercises import router as exercises_router
from services.workouts import router as workouts_router
from services.plans import router as plans_router
from services.plan_workouts import router as plan_workouts_router
from services.user_plans import router as user_plans_router

app = FastAPI()

@app.get("/")
async def get_db(db = Depends(get_db)):
    try:
        await db.command("ping")
        return {"message": "Bem vindo ao ElitePlans"}
    except Exception as e:
        print(e)
        return {"message": "Ops! Erro ao conectar-se ao banco de dados..."}

# Adicionando rotas de usuários
app.include_router(users_router)

# Adicionando rotas de exercícios
app.include_router(exercises_router)

# Adicionando rotas de treinos
app.include_router(workouts_router)

# Adicionando rotas de planos
app.include_router(plans_router)

# Adicionando rotas de treinos para planos
app.include_router(plan_workouts_router)

# Adicionando rotas de planos para usuários
app.include_router(user_plans_router)