from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponseForbidden, FileResponse, Http404
from django.views.decorators.http import require_POST
from mimetypes import guess_type
from .forms import ArquivoForm
from .models import Arquivo

# ==================== TELAS ====================

def Login(request):
    return render(request, 'samu/Login.html')

def user(request):
    return render(request, 'samu/user_list.html')

# ==================== LOGIN/LOGOUT ====================

def fazer_login(request):
    if request.method == 'POST':
        usuario = request.POST['usuario']
        senha = request.POST['senha']
        user = authenticate(request, username=usuario, password=senha)

        if user is not None:
            login(request, user)
            return redirect('adm' if user.is_staff else 'inicio')
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
            return redirect('login')

    return render(request, 'Login.html')

def sair(request):
    logout(request)
    return redirect('login')

# ==================== DASHBOARDS ====================

@login_required
def dashboard_admin(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("Acesso negado")
    return render(request, 'admin_app/ADM_inicial.html')

@login_required
def dashboard_usuario(request):
    return render(request, 'user/inicial.html')

@login_required
def adm_painel(request):
    nome_usuario = request.user.get_full_name() or request.user.username
    return render(request, 'admin_app/ADM_inicial.html', {'usr_name': nome_usuario})

@login_required
def inicial_painel(request):
    nome_usuario = request.user.get_full_name() or request.user.username
    return render(request, 'user/inicial.html', {'usr_name': nome_usuario})

@login_required
def adm_inicial(request):
    nome_usuario = request.user.get_full_name() or request.user.username
    return render(request, 'admin_app/adm_inicial.html', {'usr_name': nome_usuario})

@login_required
def inicial(request):
    nome_usuario = request.user.get_full_name() or request.user.username
    return render(request, 'user/inicial.html', {'usr_name': nome_usuario})


# ==================== ARQUIVOS ====================

@login_required
@require_POST
def adicionar_arquivo(request):
    if not request.user.is_staff:
        return JsonResponse({'erro': 'Acesso negado.'}, status=403)

    form = ArquivoForm(request.POST, request.FILES)
    if form.is_valid():
        form.save()
        return JsonResponse({'mensagem': 'Arquivo adicionado com sucesso!'})
    return JsonResponse({'erro': form.errors}, status=400)

@login_required
def pesquisar(request):
    nome = request.GET.get('nome_paciente', '')
    data = request.GET.get('data_arquivo', '')

    resultados = Arquivo.objects.all()
    if nome:
        resultados = resultados.filter(nome_paciente__icontains=nome)
    if data:
        resultados = resultados.filter(data_arquivo=data)

    return render(request, 'user/pesquisa.html', {'resultados': resultados})

@login_required
def ver_documento(request, arquivo_id):
    try:
        arquivo = Arquivo.objects.get(id=arquivo_id)
        file_path = arquivo.arquivo.path
        file = arquivo.arquivo.open()

        mime_type, _ = guess_type(file_path)
        if not mime_type:
            mime_type = 'application/pdf'

        return FileResponse(file, content_type=mime_type)
    except Arquivo.DoesNotExist:
        raise Http404("Arquivo não encontrado")

@login_required
def baixar_arquivo(request, id):
    try:
        arquivo = Arquivo.objects.get(pk=id)
        return FileResponse(arquivo.arquivo.open('rb'), as_attachment=True)
    except Arquivo.DoesNotExist:
        raise Http404("Arquivo não encontrado.")

@login_required
@require_POST
def excluir_arquivo(request, id):
    arquivo = get_object_or_404(Arquivo, id=id)
    arquivo.delete()

    nome = request.GET.get('nome_paciente', '')
    data = request.GET.get('data_arquivo', '')

    resultados = Arquivo.objects.all()
    if nome:
        resultados = resultados.filter(nome_paciente__icontains=nome)
    if data:
        resultados = resultados.filter(data_arquivo=data)

    return render(request, 'user/pesquisa.html', {'resultados': resultados})



