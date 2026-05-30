from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Definimos que vamos usar o SQLite. Ele cria um arquivo local chamado 'biblioteca.db'.
SQLALCHEMY_DATABASE_URL = "sqlite:///./biblioteca.db"

# comunicação entre o código Python e o arquivo do SQLite
# o 'check_same_thread: False' é necessário no SQLite para permitir que o FastAPI (que pode usar várias threads) 
# acesse o banco de dados sem causar erros de travamento.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
# o sessionmaker cria "conversas" com o banco de dados. Desativamos o autocommit para termos controle 
# manual de quando salvar as alterações no banco (usando db.commit()).
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# o ORM (Object-Relational Mapping) vai usar essa classe para entender 
# que os nossos modelos em Python (no models.py) devem ser transformados em tabelas reais no banco de dados.
Base = declarative_base()

# Toda vez que uma requisição HTTP (GET, POST, etc.) chegar na API, ela vai chamar essa função.
# O 'yield' entrega a sessão do banco para a rota usar. O bloco 'finally' garante que, 
# assim que a rota terminar de responder ao Front-end, a conexão com o banco será fechada por segurança.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()