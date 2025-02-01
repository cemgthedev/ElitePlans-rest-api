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
db.userplans.create_index([('user_id', 1), ('plan_id', 1)])       # Busca de ids de planos de um usuário
db.planworkouts.create_index([('plan_id', 1), ('workout_id', 1)]) # Busca de ids de treinos de um plano
db.exercises.create_index("workout_id")                           # Busca de exercícios de um treino

'''
    Obs: consultas menos comuns como usuários de um plano e planos de um treino não possuem índices de otimização.
'''

def get_db():
    return db