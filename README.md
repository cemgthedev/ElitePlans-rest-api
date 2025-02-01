# ElitePlans-rest-api
Projeto da disciplina de Desenvolvimento de Software para Persistência. Trata-se de uma REST API utilizando o framework FastAPI e Motor do python consistindo em uma aplicação para persistir dados de planos de treino personalizados no bando de dados não relacional, MongoDB.

# Executando
- Criar um ambiente virtual com o seguinte comando: python -m venv .venv
- Rodar ambiente no prompt de comando do windows: .venv\Scripts\activate
- Instalar libs: pip install fastapi uvicorn psycopg2 motor pydantic pyyaml
- Entrar na pasta src: cd src
- Executar o servidor com o seguinte comando: uvicorn main:app --reload
