document.addEventListener('DOMContentLoaded', function () {
    // Abrir modal
    document.querySelectorAll('.card')[0].addEventListener('click', () => {
        document.getElementById('addUserModal').style.display = 'block';

        // Limpa os inputs ao abrir
        document.querySelectorAll('.modal-content input')[0].value = "";
        document.querySelectorAll('.modal-content input')[1].value = "";
    });

    // Fechar modal ao clicar fora
    window.onclick = function (event) {
        const modal = document.getElementById('addUserModal');
        if (event.target == modal) {
            fecharModal();
        }
    }

    // Função para fechar modal e limpar inputs
    function fecharModal() {
        const modal = document.getElementById('addUserModal');
        modal.style.display = 'none';

        // Limpa os inputs ao fechar
        document.querySelectorAll('.modal-content input')[0].value = "";
        document.querySelectorAll('.modal-content input')[1].value = "";
    }

    window.fecharModal = fecharModal;

    // Pega o CSRF
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    const csrftoken = getCookie('csrftoken') || window.csrftoken;

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

    // Botão adicionar usuário
    document.querySelector('.add-btn').addEventListener('click', () => {
        const nome = document.querySelectorAll('.modal-content input')[0].value.trim();
        const senha = document.querySelectorAll('.modal-content input')[1].value.trim();

        fetch('/adicionar-usuario/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            credentials: 'same-origin',
            body: JSON.stringify({ nome, senha })
        })
            .then(async res => {
                const data = await parseJsonResponse(res);

                if (!res.ok || data.success === false) {
                    const message = data.msg || data.erro || 'Erro ao criar usuário.';
                    throw new Error(message);
                }

                return data;
            })
            .then(data => {
                const msgDiv = document.getElementById('mensagem');
                msgDiv.textContent = data.msg;
                msgDiv.style.display = 'block';
                msgDiv.className = data.success ? 'mensagem-sucesso' : 'mensagem-erro';

                if (data.success) {
                    fecharModal();
                }

                setTimeout(() => {
                    msgDiv.style.display = 'none';
                }, 4000);
            })
            .catch(error => {
                const msgDiv = document.getElementById('mensagem');
                msgDiv.textContent = error.message || 'Erro ao criar usuário.';
                msgDiv.style.display = 'block';
                msgDiv.className = 'mensagem-erro';

                setTimeout(() => {
                    msgDiv.style.display = 'none';
                }, 4000);
            });
    });
});
