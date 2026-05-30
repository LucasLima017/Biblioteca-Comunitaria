from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models, schemas, database

# Cria as tabelas no banco de dados ao iniciar o servidor
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="API Biblioteca Comunitária")
# mecanismo de segurança, sem isso o Front-end (rodando na porta 5500) 
# seria bloqueado pelo navegador ao tentar conversar com a API (rodando na porta 8000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # permite que qualquer origem acesse a API (ideal para desenvolvimento)
    allow_credentials=True,
    allow_methods=["*"], # permite todos os métodos HTTP (GET, POST, PUT, DELETE)
    allow_headers=["*"],
)

# o Front-end usa o GET para pedir dados à API, a resposta será empacotada e enviada como JSON
@app.get("/livros", response_model=schemas.ListaLivrosResponse)
def listar_livros(db: Session = Depends(database.get_db)): # depends injeta a conexão com o banco
    livros = db.query(models.Livro).all() # busca todos os livros no banco
    return {"dados": livros}

# busca apenas um livro específico pela URL 
@app.get("/livros/{id}", response_model=schemas.LivroResponse)
def buscar_livro(id: int, db: Session = Depends(database.get_db)):
    livro = db.query(models.Livro).filter(models.Livro.id == id).first()
    if not livro:
        # se o livro não existir aparece um erro 404 (Not Found)
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    return livro

# o POST recebe novos dados em formato JSON no body da requisição
# retorna status_code 201 (created)
@app.post("/livros", response_model=schemas.LivroResponse, status_code=status.HTTP_201_CREATED)
def adicionar_livro(livro: schemas.LivroCreate, db: Session = Depends(database.get_db)):
    novo_livro = models.Livro(**livro.dict()) # converte o JSON validado para o modelo do banco
    db.add(novo_livro)
    db.commit() # efetiva a gravação física no banco de dados
    db.refresh(novo_livro) # atualiza a variável para pegar o ID que o banco gerou
    return novo_livro

# o PUT é usado para alterar dados existentes, o front-end envia o ID na URL e o JSON de alteração
@app.put("/livros/{id}")
def atualizar_livro(id: int, livro_update: schemas.LivroUpdate, db: Session = Depends(database.get_db)):
    db_livro = db.query(models.Livro).filter(models.Livro.id == id).first()
    if not db_livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    db_livro.disponivel = livro_update.disponivel # altera apenas a disponibilidade do livro
    db.commit()
    return {"mensagem": "Status atualizado com sucesso"}

# remove um recurso do banco com base no ID recebido na URL
@app.delete("/livros/{id}")
def deletar_livro(id: int, db: Session = Depends(database.get_db)):
    db_livro = db.query(models.Livro).filter(models.Livro.id == id).first()
    if not db_livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    db.delete(db_livro) # remove da tabela
    db.commit()
    return {"mensagem": "Livro removido com sucesso"}