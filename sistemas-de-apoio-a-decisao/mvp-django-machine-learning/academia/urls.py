

from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from . import views_usuario
from . import views_treino

urlpatterns = [
    path('', views_usuario.home, name='home'),
    path('restrita/', views_usuario.area_restrita, name='area_restrita'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='/login/'), name='logout'),  # Permitir GET
    path('permissoes/', views_usuario.gerenciar_permissoes, name='gerenciar_permissoes'),
    path('usuarios/', views_usuario.usuario_list, name='usuario_list'),
    path('usuarios/novo/', views_usuario.usuario_create, name='usuario_create'),
    path('usuarios/<int:pk>/editar/', views_usuario.usuario_update, name='usuario_update'),
    path('usuarios/<int:pk>/excluir/', views_usuario.usuario_delete, name='usuario_delete'),
    path('meus-treinos/', views_usuario.meus_treinos, name='meus_treinos'),
    # Treinos
    path('treinos/', views_treino.treinos_list, name='treinos_list'),
    path('treinos/<int:pk>/', views_treino.treinos_detail, name='treinos_detail'),
    path('treinos/sugerir/', views_treino.treinos_sugerir, name='treinos_sugerir'),
    path('treinos/sugerir/<int:usuario_id>/', views_treino.treinos_sugerir, name='treinos_sugerir_para'),
    path('treinos/gerador/', views_treino.treinos_gerador, name='treinos_gerador'),
    path('treinos/salvar/', views_treino.treinos_salvar, name='treinos_salvar'),
    path('treinos/cadastrar/', views_treino.cadastrar_treino, name='cadastrar_treino'),
    path('treinos/pendentes/', views_treino.planos_pendentes, name='planos_pendentes'),
    path('treinos/plano/<int:pk>/aprovar/', views_treino.plano_aprovar, name='plano_aprovar'),
    path('treinos/plano/<int:pk>/remover/', views_treino.plano_remover, name='plano_remover'),
]
