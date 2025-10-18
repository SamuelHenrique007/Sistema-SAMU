from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json

from .models import SenhaUsuario

# ==================== TELAS ====================

def Login(request):
    return render(request, 'Login.html')

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

# ==================== USUÁRIOS ====================

@csrf_exempt
def adicionar_usuario(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        nome = data.get('nome').strip()
        senha = data.get('senha')

        if nome and senha:
            if User.objects.filter(username=nome).exists():
                return JsonResponse({'success': False, 'msg': 'Usuário já existe'}, status=400)

            user = User.objects.create_user(username=nome, password=senha)
            SenhaUsuario.objects.create(usuario=user, senha_plana=senha)
            return JsonResponse({'success': True, 'msg': 'Usuário criado com sucesso'})

        return JsonResponse({'success': False, 'msg': 'Dados incompletos'}, status=400)

    return JsonResponse({'success': False, 'msg': 'Método não permitido'}, status=405)

@login_required
def lista_usuarios(request):
    usuarios = User.objects.filter(is_superuser=False, is_staff=False)
    for user in usuarios:
        user.senha_plana = None

    return render(request, 'admin_app/user_list.html', {'usuarios': usuarios})

@login_required
def excluir_usuario(request, usuario_id):
    if not request.user.is_staff:
        return HttpResponseForbidden("Acesso negado")

    usuario = get_object_or_404(User, id=usuario_id)
    usuario.delete()
    return redirect('lista_usuarios')

@require_POST
@csrf_exempt
def deletar_usuario(request):
    data = json.loads(request.body)
    nome = data.get('nome')

    try:
        user = User.objects.get(username=nome)
        user.delete()
        return JsonResponse({'success': True, 'msg': 'Usuário excluído com sucesso'})
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'msg': 'Usuário não encontrado'})



@csrf_exempt
@login_required
def redefinir_senha(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("Acesso negado")

    if request.method == 'POST':
        data = json.loads(request.body)
        nome = data.get('nome')
        nova_senha = data.get('nova_senha')

        try:
            usuario = User.objects.get(username=nome)
            usuario.set_password(nova_senha)
            usuario.save()

            SenhaUsuario.objects.update_or_create(
                usuario=usuario,
                defaults={'senha_plana': nova_senha}
            )

            return JsonResponse({'success': True, 'msg': f'Senha de {nome} redefinida com sucesso!'})
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'msg': 'Usuário não encontrado.'}, status=404)

    return JsonResponse({'success': False, 'msg': 'Método não permitido.'}, status=405)
