# app/main.py

from fastapi import FastAPI
from . import schemas # Importa o arquivo de schemas

app = FastAPI(
    title="Estética.IO API",
    description="API para o sistema de gestão de clínica estética",
    version="0.1.0",
)

@app.get("/", response_model=schemas.MessageResponse)
async def read_root():
    """Retorna uma mensagem de boas-vindas."""
    return {"message": "Bem-vindo à API da Estética.IO!"}

@app.get("/health", response_model=schemas.MessageResponse)
async def health_check():
    """Verifica o status da API."""
    return {"status": "ok", "message": "API está funcionando!"}
