from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env, se presente
load_dotenv()

# Obtém a URI do MongoDB a partir das variáveis de ambiente
MONGO_URI = os.getenv("MONGO_URI")

# Criação de um cliente assíncrono para o MongoDB
client = AsyncIOMotorClient(MONGO_URI)

# Definição do banco de dados que será utilizado no projeto
db = client["eliteplans"]

# Criação de índices para performance das consultas mais relevantes
db.users.create_index([("name", "text")], weights={"name": 1})
db.user_plans.create_index([('seller_id', 1), ('plan_id', 1)])     # Busca de ids de planos de um vendedor
db.user_plans.create_index([('buyer_id', 1), ('plan_id', 1)])      # Busca de ids de planos de um comprador
db.plan_workouts.create_index([('plan_id', 1), ('workout_id', 1)]) # Busca de ids de treinos de um plano
db.exercises.create_index("workout_id")                           # Busca de exercícios de um treino

'''
    Obs: consultas menos comuns como usuários de um plano e planos de um treino não possuem índices de otimização.
'''

def get_db():
    return db