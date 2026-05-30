 // const livrosEncontrados = [
// //     { id: 1, titulo: "JoJo's Bizzare Adventure Stell Ball Run - Volume 1", autor: "Hirohiko Araki", disponivel: true, url_imagem: "https://d14d9vp3wdof84.cloudfront.net/image/589816272436/image_jdblsn20cd1vt929ifqeksua5m/-S897-f.webp" },

// //     { id: 2, titulo: "Kimetsu no Yaiba Demon Slayer - Volume 12", autor: "Koyoharu Gotouge", disponivel: true, url_imagem: "https://d14d9vp3wdof84.cloudfront.net/image/589816272436/image_82db58063l7kf8j47r9i0k8r6v/-S897-FWEBP" },

// //     { id: 3, titulo: "Dom Casmurro", autor: "Machado de Assis", disponivel: true, url_imagem: "https://www.livrariapolobooks.com.br/image/cache/catalog/Dom-Casmurro-600x800.jpg" },

// //     { id: 4, titulo: "Duna", autor: "Frank Herbert", disponivel: true, url_imagem: "https://m.media-amazon.com/images/I/81zN7udGRUL.jpg" },

// //     { id: 5, titulo: "Sense Life - Volume 1", autor: "Caio Ulisses", disponivel: false, url_imagem:"https://m.media-amazon.com/images/I/61gMtSihfZL._AC_UF1000,1000_QL80_.jpg"},

// //     { id: 6, titulo: "Jujutsu Kaisen - Volume 18", autor: "Gege Akutami", disponivel: true, url_imagem:"https://m.media-amazon.com/images/I/81InOZKyKSL.jpg"}
// // ];

// const container = document.getElementById('resultadosBusca');

// acima era o javaScript anterior sem a integração com o backend

const container = document.getElementById('resultadosBusca');
let todosOsLivros = [];

async function carregarLivros() {
    try {
        // O fetch faz uma requisição HTTP para a rota /livros do backend
        // como não especificamos o method ele faz um GET por padrão
        // O await faz o código esperar a resposta do servidor antes de continuar
        const resposta = await fetch('http://127.0.0.1:8000/livros');
        // A API devolve um texto no formato JSON, afunção .json() pega esse texto 
        // e transforma de volta num array/objeto que o javaScript consegue ler 
        const json = await resposta.json();
        container.innerHTML = ""; 
        todosOsLivros = json.dados;
        exibirLivros(todosOsLivros); 
    } catch (erro) {
        console.error("Erro ao buscar livros:", erro);
    }
}

function pesquisarLivro() {
    const termoPesquisa = document.getElementById('inputPesquisa').value.toLowerCase();

    const livrosFiltrados = todosOsLivros.filter(livro => 
        livro.titulo.toLowerCase().includes(termoPesquisa));

    container.innerHTML = "";
    exibirLivros(livrosFiltrados);
}

function exibirLivros(livros) {
    livros.forEach(livro => {
        const card = document.createElement('div');
        card.classList.add('card-livro');

        card.innerHTML = `
            <img src="${livro.url_imagem}" alt="${livro.titulo}">
            <h3>${livro.titulo}</h3>
            <p>${livro.autor}</p>
            <p class="${livro.disponivel ? 'status-disponivel' : 'status-indisponivel'}">
                ${livro.disponivel ? 'Disponível' : 'Indisponível'}
            </p>
            <button ${!livro.disponivel ? 'disabled' : ''} onclick="reservarLivro(${livro.id})">
                ${livro.disponivel ? 'Reservar' : 'Indisponível'}
            </button>
        `;
        container.appendChild(card);
    });
}

async function reservarLivro(id) {
    try {
        // passando o ID do livro diretamente na URL
        const resposta = await fetch(`http://127.0.0.1:8000/livros/${id}`, {
            // O PUT é o método HTTP em um RESTful para atualizar um recurso existente
            method: 'PUT',
            // O header Content-Type avisa ao backend que esta enviando um JSON
            headers: { 'Content-Type': 'application/json' },
            // usamos JSON.stringify() para converter o objeto JavaScript disponivel: false
            // em uma string com o formato JSON
            body: JSON.stringify({ disponivel: false })
        });
        if (resposta.ok) {
            alert("Livro reservado com sucesso!");
            carregarLivros(); // recarrega a lista
        }
    } catch (erro) {
        console.error("Erro ao reservar:", erro);
    }
}
carregarLivros();