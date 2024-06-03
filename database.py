from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Caminho para o arquivo do banco de dados SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# Cria uma instância do motor do banco de dados
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Cria uma instância de base de classe declarativa
Base = declarative_base()

# Cria uma função para criar sessões do banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
