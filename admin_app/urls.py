from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.fazer_login, name='login'),
    path('logout/', views.sair, name='logout'),

    path('adicionar-usuario/', views.adicionar_usuario, name='adicionar_usuario'),
    path('remover_usuario/', views.lista_usuarios, name='lista_usuarios'),
    path('excluir-usuario/<int:usuario_id>/', views.excluir_usuario, name='excluir_usuario'),
    path('deletar-usuario/', views.deletar_usuario, name='deletar_usuario'),
    path('redefinir-senha/', views.redefinir_senha, name='redefinir_senha'),

    path('dashboard/admin/', views.dashboard_admin, name='dashboard_admin'),
    path('adm/', views.adm_painel, name='adm'),
    path('adm/inicial/', views.adm_inicial, name='ADM_inicial'),

]

