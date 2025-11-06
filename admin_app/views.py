from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.http import require_POST
import json

from django.utils.translation import gettext_lazy as _

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

@login_required
@require_POST
def adicionar_usuario(request):
    if not request.user.is_staff:
        return JsonResponse({'success': False, 'msg': _('Acesso negado.')}, status=403)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'msg': _('Erro ao interpretar os dados enviados!')}, status=400)

    nome = data.get('nome', '').strip()
    senha = data.get('senha', '').strip()

    if not nome or not senha:
        return JsonResponse({'success': False, 'msg': _('Preencha todos os campos!')}, status=400)

    if User.objects.filter(username__iexact=nome).exists():
        return JsonResponse({'success': False, 'msg': _("O usuário '{name}' já existe!").format(name=nome)}, status=400)

    try:
        User.objects.create_user(username=nome, password=senha)
    except Exception:
        return JsonResponse({'success': False, 'msg': _('Erro ao criar usuário.')}, status=500)

    return JsonResponse({'success': True, 'msg': _("Usuário '{name}' criado com sucesso!").format(name=nome)})

@login_required
def lista_usuarios(request):
    usuarios = User.objects.filter(is_superuser=False, is_staff=False)

    return render(request, 'admin_app/user_list.html', {'usuarios': usuarios})

@login_required
@require_POST
def excluir_usuario(request, usuario_id):
    if not request.user.is_staff:
        return HttpResponseForbidden("Acesso negado")

    usuario = get_object_or_404(User, id=usuario_id)
    usuario.delete()
    return redirect('lista_usuarios')

@login_required
@require_POST
def deletar_usuario(request):
    if not request.user.is_staff:
        return JsonResponse({'success': False, 'msg': _('Acesso negado.')}, status=403)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'msg': _('Erro ao interpretar os dados enviados!')}, status=400)

    nome = data.get('nome', '').strip()
    if not nome:
        return JsonResponse({'success': False, 'msg': _('Informe o nome do usuário.')}, status=400)

    try:
        user = User.objects.get(username=nome)
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'msg': _('Usuário não encontrado')}, status=404)

    user.delete()
    return JsonResponse({'success': True, 'msg': _('Usuário excluído com sucesso')})



@login_required
@require_POST
def redefinir_senha(request):
    if not request.user.is_staff:
        return JsonResponse({'success': False, 'msg': _('Acesso negado.')}, status=403)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'msg': _('Erro ao interpretar os dados enviados!')}, status=400)

    nome = data.get('nome', '').strip()
    nova_senha = data.get('nova_senha', '').strip()

    if not nome or not nova_senha:
        return JsonResponse({'success': False, 'msg': _('Preencha todos os campos!')}, status=400)

    try:
        usuario = User.objects.get(username=nome)
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'msg': _('Usuário não encontrado.')}, status=404)

    usuario.set_password(nova_senha)
    usuario.save()

    return JsonResponse({'success': True, 'msg': _('Senha de {name} redefinida com sucesso!').format(name=nome)})
