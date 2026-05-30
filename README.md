Biblioteca Digital - API RESTful e Front-end

---------------------------------------------

Este projeto consiste em uma aplicação de Biblioteca Digital, composta por uma **API RESTful** desenvolvida em Python (FastAPI) e um **Front-end** dinâmico criado com HTML, CSS e JavaScript 

Tecnologias Utilizadas
- Back-end: Python, FastAPI, Uvicorn
- Banco de Dados: SQLite (via SQLAlchemy ORM)
- Validação de Dados: Pydantic
- Front-end:  HTML5, CSS e JavaScript 

---

Como Executar o Projeto?

Rodando o Back-end (API)
------------------------
Certifique-se de ter o Python instalado. No terminal, dentro da pasta do projeto, instale as dependências e inicie o servidor:

```bash
# Instalação das dependências
pip install fastapi uvicorn sqlalchemy pydantic

# Iniciando o servidor na porta 8000
uvicorn main:app --reload