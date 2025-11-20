// ==================== MODAL DE VISUALIZAÇÃO ====================

function abrirModalVerDados(nome) {
    console.log("Abrindo modal de:", nome);

    const spanNome = document.getElementById("verNome");
    const modal = document.getElementById("modalVerDados");

    if (!spanNome || !modal) {
        console.error("Elemento verNome ou modalVerDados não encontrado no DOM.");
        return;
    }

    spanNome.textContent = nome;

    // Exibir modal centralizado (usa flex no CSS)
    modal.style.display = "flex";
}

function fecharModalVerDados() {
    const modal = document.getElementById("modalVerDados");
    if (modal) {
        modal.style.display = "none";
    }
}

// Fecha o modal ao clicar fora
window.onclick = function (event) {
    const modal = document.getElementById("modalVerDados");
    if (modal && event.target === modal) {
        modal.style.display = "none";
    }
};


// ==================== REDEFINIR SENHA ====================

function redefinirSenha() {
    const nomeSpan = document.getElementById("verNome");
    const inputSenha = document.getElementById("redefinirSenha");

    if (!nomeSpan || !inputSenha) {
        console.error("Campos do modal não encontrados.");
        return;
    }

    const nome = nomeSpan.textContent;
    const novaSenha = inputSenha.value.trim();

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
            fetch("/adm/redefinir-senha/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    nome: nome,
                    nova_senha: novaSenha,
                }),
            })
                .then((res) => res.json())
                .then((data) => {
                    if (data.success) {
                        Swal.fire({
                            icon: "success",
                            title: data.msg,
                            confirmButtonColor: "#4CAF50"
                        }).then(() => {
                            // limpa o campo
                            inputSenha.value = "";
                            // fecha o modal
                            fecharModalVerDados();
                        });
                    } else {
                        Swal.fire({
                            icon: "error",
                            title: data.msg || "Erro ao redefinir senha",
                            confirmButtonColor: "#4CAF50"
                        });
                    }
                })
                .catch((error) => {
                    console.error(error);
                    Swal.fire({
                        icon: "error",
                        title: "Erro na requisição!",
                        text: "Tente novamente.",
                        confirmButtonColor: "rgba(255, 0, 0, 1)"
                    });
                });
        }
    });
}
