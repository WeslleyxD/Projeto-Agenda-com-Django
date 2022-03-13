from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('sobre/', views.sobre, name='sobre'),
    path('cadastrar/', views.cadastrar, name='cadastrar'),
    path('login/', views.login_view, name='login'),
    path('contatos/', views.contatos, name='contatos'),
    path('logout/', views.logout_view, name='logout'),
    path('cadastrar_contato/', views.cadastrar_contato, name='cadastrar_contato'),
    path('contato/<int:contato_id>/', views.ver_contato, name='ver_contato'),
    path('excluir/<int:contato_id>/', views.excluir_contato, name='excluir_contato'),
    path('update/<int:contato_id>/', views.update_contato, name='update_contato'),
]
