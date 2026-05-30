from pydantic import BaseModel
from typing import List, Optional

# schemas cuidam da API e do formato JSON
# eles garantem que os dados enviados pelo Front-end estão no tipo certo

# classe base com os atributos comuns de um livro
class LivroBase(BaseModel):
    titulo: str
    autor: str
    url_imagem: str
    disponivel: bool = True

# usado para criar um livro via POST (Não pedimos o ID pois o banco de dados gera sozinho)
class LivroCreate(LivroBase):
    pass
# Usado para ATUALIZAR via PUT
# neste projeto, o front-end só altera se o livro está disponível ou não
class LivroUpdate(BaseModel):
    disponivel: bool
# Usado para devolver os dados completos do livro para o Front-end
class LivroResponse(LivroBase):
    id: int #ID obrigatório porque já existe no banco

    # 'from_attributes = True' ensina o Pydantic a ler o objeto 
    # do banco de dados e convertê-lo em formato JSON válido para a internet
    class Config:
        from_attributes = True
# Usado para devolver a lista de livros, o front-end espera um objeto JSON com a chave "dados"
class ListaLivrosResponse(BaseModel):
    dados: List[LivroResponse]