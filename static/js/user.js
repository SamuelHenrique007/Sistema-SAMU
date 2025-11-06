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

// ==================== MODAL DE VISUALIZAÇÃO ====================

function abrirModalVerDados(nome) {
    console.log("Abrindo modal de:", nome);
    console.log(document.getElementById("verNome"));
    document.getElementById("verNome").textContent = nome;
    //document.getElementById("verEmail").textContent = "••••••"; // apenas máscara
    document.getElementById("modalVerDados").style.display = "block";
}

function fecharModalVerDados() {
    document.getElementById("modalVerDados").style.display = "none";
}

// Fecha o modal ao clicar fora
window.onclick = function (event) {
    const modal = document.getElementById("modalVerDados");
    if (event.target === modal) {
        modal.style.display = "none";
    }
};

// ==================== REDEFINIR SENHA ====================

function redefinirSenha() {
    const nome = document.getElementById("verNome").textContent;
    const novaSenha = document.getElementById("redefinirSenha").value.trim();

    if (novaSenha === "") {
        Swal.fire({
            icon: "warning",
            title: "Digite uma nova senha!",
            confirmButtonColor: "#4CAF50"
        });
        return;
    }

    Swal.fire({
        title: "Confirmar redefinição?",
        text: `A senha de "${nome}" será alterada.`,
        icon: "question",
        showCancelButton: true,
        confirmButtonText: "Sim, redefinir",
        cancelButtonText: "Cancelar",
        confirmButtonColor: "#4CAF50",
        cancelButtonColor: "#d33"
    }).then((result) => {
        if (result.isConfirmed) {
            const csrfToken = getCsrfToken();
            if (!csrfToken) {
                Swal.fire({
                    icon: "error",
                    title: "Sessão inválida",
                    text: "Não foi possível validar sua sessão. Recarregue a página e tente novamente.",
                    confirmButtonColor: "#d33"
                });
                return;
            }

            fetch("/redefinir-senha/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken,
                },
                credentials: 'same-origin',
                body: JSON.stringify({
                    nome: nome,
                    nova_senha: novaSenha,
                }),
            })
                .then(async (res) => {
                    const data = await parseJsonResponse(res);

                    if (!res.ok || data.success === false) {
                        const message = data.msg || 'Erro ao redefinir senha.';
                        throw new Error(message);
                    }

                    return data;
                })
                .then((data) => {
                    Swal.fire({
                        icon: "success",
                        title: data.msg,
                        confirmButtonColor: "#4CAF50"
                    });
                    document.getElementById("redefinirSenha").value = "";
                })
                .catch((error) => {
                    Swal.fire({
                        icon: "error",
                        title: "Erro na requisição!",
                        text: error.message || error,
                        confirmButtonColor: "#d33",
                    });
                });
        }
    });
}
