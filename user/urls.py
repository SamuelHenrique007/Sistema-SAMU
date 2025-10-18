from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('', views.fazer_login, name='login'),
    path('logout/', views.sair, name='logout'),

    path('dashboard/usuario/', views.dashboard_usuario, name='dashboard_usuario'),

    path('inicio/', views.inicial_painel, name='inicio'),
    path('inicial/', views.inicial, name='inicial'),

    path('adicionar/', views.adicionar_arquivo, name='adicionar_arquivo'),
    path('pesquisar/', views.pesquisar, name='pesquisar'),  
    path('ver-documento/<int:arquivo_id>/', views.ver_documento, name='ver_documento'),
    path('excluir/<int:id>/', views.excluir_arquivo, name='excluir_arquivo'),
    path('baixar/<int:id>/', views.baixar_arquivo, name='baixar_arquivo'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
