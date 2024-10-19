from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Tarefas
from .serializers import TarefasSerializer
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination

# Define uma classe para lidar com a paginação
class PaginacaoTarefas(PageNumberPagination):
    page_size = 10

# Define uma função para lidar com a lista de tarefas
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def lista_tarefas(request):
    tarefas = Tarefa.objects.filter(usuario=request.user)
    status_filter = request.query_params.get('completed')
    if status_filter is not None:
        tarefas = tarefas.filter(completed=status_filter.lower() == 'true')
    paginator = PaginacaoTarefas()
    paginated_tarefas = paginator.paginate_queryset(tarefas, request)
    serializer = TarefaSerializer(paginated_tarefas, many=True)
    return paginator.get_paginated_response(serializer.data)

# Define uma função para criar uma nova tarefa
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def criar_tarefa(request):
    serializer = TarefaSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(usuario=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Define uma função para lidar com os detalhes de uma tarefa
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def detalhe_tarefa(request, id):
    tarefa = get_object_or_404(Tarefa, id=id, usuario=request.user)
    if request.method == 'GET':
        serializer = TarefaSerializer(tarefa)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = TarefaSerializer(tarefa, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        tarefa.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)