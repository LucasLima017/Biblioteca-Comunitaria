from sqlalchemy import Column, Integer, String, Boolean
from .database import Base

# o modelo define a estrutura da tabela real lá no SQLite
# o ORM (Object-Relational Mapping) traduz as classes do Python para as tabelas que o banco entende
class Livro(Base):
    __tablename__ = "livros"

# primary_key=True diz que este é o identificador único (o ID do livro)
# index=True ajuda o banco a buscar esse ID mais rápido nas consultas
    id = Column(Integer, primary_key=True, index=True)
    # nullable=False significa que esses campos sõ obrigatórios
    titulo = Column(String, nullable=False)
    autor = Column(String, nullable=False)
    url_imagem = Column(String, nullable=False)
    # default=True faz com que, se ninguém passar outra informação o livro seja cadastrado como disponível
    disponivel = Column(Boolean, default=True)