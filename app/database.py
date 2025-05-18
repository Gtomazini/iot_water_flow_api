from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging
import os
from dotenv import load_dotenv
from pathlib import Path

base_dir = Path(__file__).resolve().parent.parent
env_path = base_dir / "keys.env"

load_dotenv(env_path)

# Obter URL do banco de dados
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    logging.error("DATABASE_URL não encontrada nas variáveis de ambiente")
    raise ValueError("DATABASE_URL não está definida no arquivo .env")

try:
    engine = create_engine(DATABASE_URL)
    # Teste de conexão
    with engine.connect() as conn:
        pass
    logging.info("Conexão com o banco de dados estabelecida com sucesso!")
except Exception as e:
    logging.error(f"Erro ao conectar ao banco de dados: {e}")
    raise

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Função para obter a sessão do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()