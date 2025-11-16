# admin_app/urls.py
from django.urls import path
from . import views

app_name = "admin_app"

urlpatterns = [
    path('login/', views.fazer_login, name='login'),
    path('logout/', views.sair, name='logout'),

    path('adicionar-usuario/', views.adicionar_usuario, name='adicionar_usuario'),
    path('remover_usuario/', views.lista_usuarios, name='lista_usuarios'),
    path('excluir-usuario/<int:usuario_id>/', views.excluir_usuario, name='excluir_usuario'),
    path('deletar-usuario/', views.deletar_usuario, name='deletar_usuario'),
    path('redefinir-senha/', views.redefinir_senha, name='redefinir_senha'),

    # painel admin principal: /adm/painel/
    path('painel/', views.adm_painel, name='adm'),

    path('inicial/', views.adm_inicial, name='adm_inicial'),
]
