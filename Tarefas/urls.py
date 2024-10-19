from django.urls import path
from . import views

urlpatterns = [
    path('tarefas/', views.lista_tarefas, name='tarefas-list'),
    path('tarefas/<int:id>/', views.detalhe_tarefa, name='tarefas-detail'),
    path('tarefas/create/', views.criar_tarefa, name='ta-create'),
]