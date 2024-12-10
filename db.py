# db.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configuração do banco de dados SQLite
DATABASE_URL = "sqlite:///autoroles.db"

# Criação da base de dados e da sessão
Base = declarative_base()

def get_session():
    engine = create_engine(DATABASE_URL, echo=True)
    Session = sessionmaker(bind=engine)
    return Session()

def create_db():
    engine = create_engine(DATABASE_URL, echo=True)
    Base.metadata.create_all(engine)
