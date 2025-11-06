function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) {
        return parts.pop().split(';').shift();
    }
    return null;
}

function getCsrfToken() {
    return getCookie('csrftoken') || window.csrftoken || '';
}

async function parseJsonResponse(response) {
    const contentType = response.headers.get('content-type') || '';
    if (!contentType.includes('application/json')) {
        const text = await response.text();
        throw new Error(text || 'Resposta inesperada do servidor.');
    }

    try {
        return await response.json();
    } catch (error) {
        throw new Error('Erro ao interpretar a resposta do servidor.');
    }
}

function sair() {
    mostrarMensagem("Saindo do sistema...", "sucesso");
}

window.onload = () => {
    const track = document.querySelector('.carousel-track');
    const slides = document.querySelectorAll('.carousel-slide');
    let currentIndex = 0;
    const totalSlides = slides.length;
    const slidesPerView = 3;

    function moveToNextSlide() {
        currentIndex++;
        if (currentIndex > totalSlides - slidesPerView) {
            currentIndex = 0;
        }
        const offset = -(100 / slidesPerView) * currentIndex;
        track.style.transform = `translateX(${offset}%)`;
    }

    setInterval(moveToNextSlide, 3000);
};

// ===============================
// 🧩 CONTROLE DE MODAIS
// ===============================

function abrirModal() {
    document.getElementById("modalAdicionar").style.display = "block";

    // 🔧 Garante que o botão não tenha múltiplos listeners
    const oldBtn = document.querySelector(".btn-adicionar");
    const newBtn = oldBtn.cloneNode(true);
    oldBtn.replaceWith(newBtn);

    // Reatribui o evento ao novo botão
    newBtn.addEventListener("click", adicionarArquivo);
}

function abrirModalPesquisar() {
    document.getElementById("modalPesquisar").style.display = "block";
}

function fecharModal() {
    const modais = document.querySelectorAll('.modal');
    modais.forEach(modal => {
        modal.style.display = 'none';
    });
}

// Fecha modal ao clicar fora dele
window.onclick = function (event) {
    const modais = document.querySelectorAll('.modal');
    modais.forEach(modal => {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });
};

// ===============================
// 📁 ADICIONAR ARQUIVO (fetch)
// ===============================

async function adicionarArquivo() {
    const nomePaciente = document.querySelector("#nomePaciente").value.trim();
    const dataArquivo = document.querySelector("#dataArquivo").value;
    const arquivoInput = document.querySelector("#arquivoInput");

    if (!nomePaciente) return mostrarMensagem("Por favor, preencha o nome do paciente.", "erro");
    if (!dataArquivo) return mostrarMensagem("Por favor, selecione a data do arquivo.", "erro");
    if (!arquivoInput.files.length) return mostrarMensagem("Selecione um arquivo.", "erro");

    const formData = new FormData();
    formData.append("nome_paciente", nomePaciente);
    formData.append("data_arquivo", dataArquivo);
    formData.append("arquivo", arquivoInput.files[0]);

    try {
        const csrfToken = getCsrfToken();
        if (!csrfToken) {
            throw new Error('Não foi possível validar sua sessão. Recarregue a página e tente novamente.');
        }

        const response = await fetch("/adicionar/", {
            method: "POST",
            body: formData,
            credentials: 'same-origin',
            headers: {
                'X-CSRFToken': csrfToken,
            },
        });

        const result = await parseJsonResponse(response);

        if (response.ok && !result.erro) {
            mostrarMensagem(result.mensagem || "Arquivo adicionado com sucesso!", "sucesso");
            fecharModal();

            // Limpa campos
            document.querySelector("#nomePaciente").value = "";
            document.querySelector("#dataArquivo").value = "";
            arquivoInput.value = "";
            document.getElementById("nomeArquivoSelecionado").textContent = "Nenhum arquivo selecionado";
        } else {
            const mensagemErro = result.mensagem || result.msg || result.erro || "Erro ao adicionar o arquivo.";
            mostrarMensagem(mensagemErro, "erro");
        }
    } catch (err) {
        mostrarMensagem("Erro ao enviar: " + (err.message || err), "erro");
    }
}

// ===============================
// 📂 ATUALIZA NOME DO ARQUIVO
// ===============================
document.getElementById("arquivoInput").addEventListener("change", function () {
    const nomeArquivo = this.files.length > 0 ? this.files[0].name : "Nenhum arquivo selecionado";
    document.getElementById("nomeArquivoSelecionado").textContent = nomeArquivo;
});

// ===============================
// 🔍 PESQUISAR ARQUIVO
// ===============================
function pesquisarArquivo() {
    const nome = document.querySelector("#pesquisarNomePaciente").value;
    const data = document.querySelector("#pesquisarDataArquivo").value;

    fecharModal();

    let url = '/pesquisar/?';
    if (nome) url += `nome_paciente=${encodeURIComponent(nome)}&`;
    if (data) url += `data_arquivo=${encodeURIComponent(data)}&`;

    window.location.href = url;
}

// ===============================
// 💬 MENSAGEM FLUTUANTE
// ===============================
function mostrarMensagem(texto, tipo = 'sucesso') {
    const msgDiv = document.getElementById('mensagem');
    msgDiv.textContent = texto;
    msgDiv.style.display = 'block';
    msgDiv.className = tipo === 'sucesso' ? 'mensagem-sucesso' : 'mensagem-erro';

    setTimeout(() => {
        msgDiv.style.display = 'none';
    }, 4000);
}
