from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login/', views.login, name = 'login'),
    path('cadastro/', views.cadastro, name = 'cadastro'),
    path('home/', views.home, name = 'home'),
    path('lancar/', views.lancar, name = 'lancar'),
    path('alterar/', views.alterar, name = 'alterar'),
    path('visualizar/', views.visualizar, name = 'visualizar'),
    path('logout/', views.logout, name = 'logout'),
    path('excluir_verificacao/<int:pk>', views.excluir_verificacao, name = 'excluir_verificacao'),
    path('excluir/<int:pk>', views.excluir, name = 'excluir'),
    path('editar_verificacao/<int:pk>', views.editar_verificacao, name = 'editar_verificacao'),
    path('editar/<int:pk>', views.editar, name = 'editar'),
    path('sobre/', views.sobre, name = 'sobre'),
    path('contato/', views.contato, name = 'contato')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)