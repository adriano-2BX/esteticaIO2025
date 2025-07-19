# app/init_db.py

from .database import engine, Base
from . import models  # Importa todos os modelos definidos em models.py

def create_tables():
    print("Tentando criar tabelas no banco de dados...")
    try:
        # Cria todas as tabelas definidas nos modelos que herdam de Base
        # Agora, Base.metadata.create_all() vai encontrar suas classes de modelo
        Base.metadata.create_all(bind=engine)
        print("Tabelas criadas com sucesso ou já existentes.")
    except Exception as e:
        print(f"Erro ao criar tabelas: {e}")
        # Em um ambiente real, você pode querer logar esse erro mais detalhadamente
        # e talvez ter uma lógica para tentar novamente ou notificar.
        raise # Re-levanta a exceção para que o chamador possa lidar com ela

# Se este script for executado diretamente
if __name__ == "__main__":
    create_tables()
