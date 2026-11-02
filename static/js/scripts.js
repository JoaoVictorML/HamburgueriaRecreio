// Dados dos Produtos baseados no cardápio
const produtos = [
    { id: 1, nome: "Double Burguer", categoria: "especiais", preco: 20.00, desc: "2 carnes artesanais, queijo duplo, bacon crocante, salada completa e molho especial." },
    { id: 2, nome: "Burguer Calabresa", categoria: "especiais", preco: 18.00, desc: "Carne artesanal, fatias de calabresa selada, queijo derretido e maionese da casa." },
    { id: 3, nome: "Tropical Burguer", categoria: "especiais", preco: 18.00, desc: "Carne artesanal, queijo cheddar, abacaxi grelhado, bacon e molho especial." },
    { id: 4, nome: "Double Bacon", categoria: "especiais", preco: 22.00, desc: "2 carnes artesanais, cheddar duplo, dobro de bacon crocante e molho barbecue." },
    { id: 5, nome: "Imperador", categoria: "especiais", preco: 19.00, desc: "Carne artesanal de 150g, queijo coalho grelhado, melaço e bacon crocante." },
    { id: 6, nome: "Recreio Burguer", categoria: "especiais", preco: 22.00, desc: "O carro chefe! Carne artesanal, cheddar, bacon, picles, cebola roxa e molho Recreio." },
    { id: 7, nome: "Serra Verde Burguer", categoria: "especiais", preco: 25.00, desc: "2 carnes artesanais, muito queijo, bacon, salada fresca e creme de gorgonzola." },
    { id: 8, nome: "X-Burguer Tradicional", categoria: "tradicionais", preco: 12.00, desc: "Carne tradicional, queijo derretido e pão brioche macio." },
    { id: 9, nome: "X-Salada Tradicional", categoria: "tradicionais", preco: 14.00, desc: "Carne tradicional, queijo, alface, tomate e maionese." },
    { id: 10, nome: "Combo 1 - Recreio", categoria: "combos", preco: 30.00, desc: "1 Recreio Burguer + Batata Frita Individual + Refrigerante Lata." }
];

let carrinho = [];

// Elementos do DOM
const gridProdutos = document.getElementById('gridProdutos');
const categoriasContainer = document.getElementById('categorias');
const itensCarrinho = document.getElementById('itensCarrinho');
const carrinhoVazio = document.getElementById('carrinhoVazio');
const resumoCarrinho = document.getElementById('resumoCarrinho');
const valorTotal = document.getElementById('valorTotal');
const navToggle = document.getElementById('navToggle');
const navBar = document.getElementById('navBar');
const btnEnviarWhatsapp = document.getElementById('btnEnviarWhatsapp');

// Renderizar Produtos
function renderizarProdutos(categoriaFiltro = 'todos') {
    gridProdutos.innerHTML = '';
    
    const produtosFiltrados = categoriaFiltro === 'todos' 
        ? produtos 
        : produtos.filter(p => p.categoria === categoriaFiltro);

    produtosFiltrados.forEach(produto => {
        const card = document.createElement('div');
        card.className = 'card-produto';
        card.innerHTML = `
            <div>
                <span class="card-tag">${produto.categoria}</span>
                <h3 class="card-titulo">${produto.nome}</h3>
                <p class="card-descricao">${produto.desc}</p>
            </div>
            <div class="card-rodape">
                <span class="card-preco">R$ ${produto.preco.toFixed(2).replace('.', ',')}</span>
                <button class="btn-add" onclick="adicionarAoCarrinho(${produto.id})">Adicionar</button>
            </div>
        `;
        gridProdutos.appendChild(card);
    });
}

// Filtro de Categorias
categoriasContainer.addEventListener('click', (e) => {
    if (e.target.classList.contains('btn-categoria')) {
        document.querySelectorAll('.btn-categoria').forEach(b => b.classList.remove('ativo'));
        e.target.classList.add('ativo');
        renderizarProdutos(e.target.dataset.cat);
    }
});

// Adicionar item ao Carrinho
function adicionarAoCarrinho(id) {
    const produto = produtos.find(p => p.id === id);
    const itemExistente = carrinho.find(item => item.id === id);

    if (itemExistente) {
        itemExistente.qtd++;
    } else {
        carrinho.push({ ...produto, qtd: 1 });
    }
    atualizarCarrinho();
}

// Alterar Quantidade no Carrinho
function alterarQtd(id, delta) {
    const item = carrinho.find(item => item.id === id);
    if (item) {
        item.qtd += delta;
        if (item.qtd <= 0) {
            carrinho = carrinho.filter(i => i.id !== id);
        }
    }
    atualizarCarrinho();
}

// Atualizar Interface do Carrinho
function atualizarCarrinho() {
    itensCarrinho.innerHTML = '';
    
    if (carrinho.length === 0) {
        carrinhoVazio.style.display = 'block';
        resumoCarrinho.style.display = 'none';
        return;
    }

    carrinhoVazio.style.display = 'none';
    resumoCarrinho.style.display = 'block';

    let total = 0;

    carrinho.forEach(item => {
        total += item.preco * item.qtd;
        const div = document.createElement('div');
        div.className = 'item-carrinho';
        div.innerHTML = `
            <div class="item-info">
                <span class="item-nome">${item.nome}</span>
                <span class="item-preco">R$ ${(item.preco * item.qtd).toFixed(2).replace('.', ',')}</span>
            </div>
            <div class="item-controles">
                <button class="btn-qtd" onclick="alterarQtd(${item.id}, -1)">-</button>
                <span>${item.qtd}</span>
                <button class="btn-qtd" onclick="alterarQtd(${item.id}, 1)">+</button>
            </div>
        `;
        itensCarrinho.appendChild(div);
    });

    valorTotal.textContent = `R$ ${total.toFixed(2).replace('.', ',')}`;
}

// Enviar Pedido para o WhatsApp
btnEnviarWhatsapp.addEventListener('click', () => {
    const nome = document.getElementById('nomeCliente').value.trim();
    const endereco = document.getElementById('enderecoCliente').value.trim();
    const pagamento = document.getElementById('pagamentoCliente').value;

    if (!nome || !endereco) {
        alert('Por favor, preencha seu nome e o endereço de entrega.');
        return;
    }

    let mensagem = `*NOVO PEDIDO - HAMBURGUERIA RECREIO*\n\n`;
    mensagem += `*Cliente:* ${nome}\n`;
    mensagem += `*Endereço:* ${endereco}\n`;
    mensagem += `*Pagamento:* ${pagamento}\n\n`;
    mensagem += `*ITENS:* \n`;

    let total = 0;
    carrinho.forEach(item => {
        const subtotal = item.preco * item.qtd;
        total += subtotal;
        mensagem += `• ${item.qtd}x ${item.nome} - R$ ${subtotal.toFixed(2).replace('.', ',')}\n`;
    });

    mensagem += `\n*TOTAL:* R$ ${total.toFixed(2).replace('.', ',')}`;

    const telefone = "5588993810676";
    const url = `https://wa.me/${telefone}?text=${encodeURIComponent(mensagem)}`;
    window.open(url, '_blank');
});

// Menu Mobile
navToggle.addEventListener('click', () => {
    navBar.classList.toggle('aberto');
});

// Inicialização
renderizarProdutos();