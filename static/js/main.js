const cache = new Map();

async function carregar(nome) {
  if (!cache.has(nome)) {
    const resposta = await fetch(`/static/components/${nome}.html`);
    if (!resposta.ok) throw new Error(`Componente "${nome}" não encontrado`);
    cache.set(nome, await resposta.text());
  }
  return cache.get(nome);
}

function escapeHtml(t) {
  return String(t)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;')
    .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

async function renderizar(modelo, dados = {}, pilha = []) {
  const reImport = /\{%\s*import\s+([\w-]+)\s*%\}/g;
  const nomes = [...new Set([...modelo.matchAll(reImport)].map((m) => m[1]))];

  const parciais = {};
  await Promise.all(
    nomes.map(async (nome) => {
      if (pilha.includes(nome)) throw new Error(`Import circular: ${[...pilha, nome].join(' > ')}`);
      parciais[nome] = await renderizar(await carregar(nome), dados, [...pilha, nome]);
    })
  );

  return modelo
    .replace(reImport, (_, nome) => parciais[nome])
    .replace(/\{\{\s*([\w.]+)\s*\}\}/g, (_, caminho) => {
      const valor = caminho.split('.').reduce((o, k) => o?.[k], dados);
      return valor == null ? '' : escapeHtml(valor);
    });
}

// Monta a página: troca cada <div data-import="header"> pelo componente
async function montarPagina(dados = {}) {
  const alvos = document.querySelectorAll('[data-import]');
  for (const el of alvos) {
    el.innerHTML = await renderizar(`{%import ${el.dataset.import}%}`, dados);
  }
}

montarPagina({ usuario: { nome: 'Maria' } });


const botao = document.querySelector('.nav-toggle');
const menu = document.querySelector('#menu');

if (botao && menu) {
    botao.addEventListener('click', () => {
        const aberto = menu.classList.toggle('aberto');
        botao.setAttribute('aria-expanded', aberto);
        botao.textContent = aberto ? '✕' : '☰';
    });
}