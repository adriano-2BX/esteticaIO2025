# app/main.py

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from . import schemas, models, auth # Importa os módulos de schemas, models e auth
from .database import get_db, engine # Importa get_db e engine para criar tabelas

# --- INSTÂNCIA DO FASTAPI (MOVIDA PARA CIMA) ---
app = FastAPI(
    title="Estética.IO API",
    description="API para o sistema de gestão de clínica estética",
    version="0.1.0",
)

# --- Criação de Tabelas no Startup (Instalador) ---
@app.on_event("startup")
def on_startup():
    """Função executada na inicialização da aplicação."""
    print("Iniciando a aplicação e verificando/criando tabelas do banco de dados...")
    try:
        # Cria todas as tabelas se elas não existirem
        models.Base.metadata.create_all(bind=engine)
        print("Tabelas do banco de dados verificadas/criadas com sucesso.")

        # Opcional: Criar um usuário admin padrão se não existir
        db = next(get_db()) # Obtém uma sessão de DB
        if not auth.get_user_by_email(db, email="admin@estetica.com"):
            hashed_password = auth.get_password_hash("1234")
            admin_user = models.User(
                email="admin@estetica.com",
                password_hash=hashed_password,
                name="Administrador",
                role="admin"
            )
            db.add(admin_user)
            db.commit()
            db.refresh(admin_user)
            print("Usuário administrador padrão criado com sucesso: admin@estetica.com")
        else:
            print("Usuário administrador padrão já existe.")
        db.close()
    except Exception as e:
        print(f"ERRO CRÍTICO na inicialização do banco de dados: {e}")
        # Em produção, você pode querer que a aplicação falhe ao iniciar se o DB não estiver pronto.
        raise # Re-levanta a exceção para que o EasyPanel possa reportar a falha.


# --- Endpoints de Autenticação ---
@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Endpoint para autenticação de usuário.
    Recebe `username` (email) e `password`.
    Retorna um token JWT se as credenciais forem válidas.
    """
    user = auth.get_user_by_email(db, email=form_data.username)
    if not user or not auth.verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha inválidos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email, "role": user.role}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=schemas.UserResponse)
async def read_users_me(current_user: models.User = Depends(auth.get_current_user)):
    """
    Retorna as informações do usuário logado.
    Esta rota é protegida e exige um token JWT válido.
    """
    return current_user

# Exemplo de rota protegida apenas para admin
@app.get("/admin-only", response_model=schemas.MessageResponse)
async def read_admin_only_data(current_admin: models.User = Depends(auth.get_current_admin_user)):
    """
    Endpoint de exemplo acessível apenas por usuários com role 'admin'.
    """
    return {"message": f"Olá, {current_admin.name}! Você tem acesso de admin."}

# --- Rotas de Saúde da Aplicação (Mantidas no final para organização) ---
@app.get("/", response_model=schemas.MessageResponse)
async def read_root():
    """Retorna uma mensagem de boas-vindas."""
    return {"message": "Bem-vindo à API da Estética.IO!"}

@app.get("/health", response_model=schemas.MessageResponse)
async def health_check():
    """Verifica o status da API."""
    return {"status": "ok", "message": "API está funcionando!"}
