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
            fetch("/redefinir-senha/", {
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
                    Swal.fire({
                        icon: data.success ? "success" : "error",
                        title: data.msg,
                        confirmButtonColor: "#4CAF50"
                    });
                    if (data.success) {
                        document.getElementById("redefinirSenha").value = "";
                    }
                })
                .catch((error) => {
                    Swal.fire({
                        icon: "error",
                        title: "Erro na requisição!",
                        text: error,
                        confirmButtonColor: "#d33"
                    });
                });
        }
    });
}
