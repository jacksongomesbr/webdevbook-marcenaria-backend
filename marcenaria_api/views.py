from django.contrib.auth import authenticate
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, response, status, decorators, generics, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticatedOrReadOnly
from .serializers import *
from .models import *


# Create your views here.


@api_view(['POST'])
@permission_classes((AllowAny,))
def checklogin_view(request):
    """
    Realiza a autenticação, verificando se o `username` e `password` informados estão corretos.

    Retorna um objeto conforme o resultado da autenticação.

    Se a autenticação estiver correta, retorna código `200` e um objeto:

    ```json
    {
        "situacao": "ok",
        "mensagem": "Autenticação realizada com sucesso"
    }
    ```

    Se a autenticação estiver incorreta, retorna código `403` e um objeto:

    ```json
    {
        "situacao": "erro",
        "mensagem": "Nome de usuário ou senha incorretos"
    }
    ```
    """
    username = request.data.get('username', None)
    password = request.data.get('password', None)
    user = authenticate(username=username, password=password)
    if user:
        resposta = {
            'situacao': 'ok',
            'mensagem': 'Autenticação realizada com sucesso',
        }
        return Response(resposta, status=200)
    else:
        resposta = {
            'situacao': 'erro',
            'mensagem': 'Nome de usuário ou senha incorretos',
        }
        return Response(resposta, status=403)


class UserViewSet(viewsets.ModelViewSet):
    """
    Provides basic CRUD functions for the User model
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    ordering_fields = '__all__'
    filter_fields = ('username', 'email', 'groups',)
    permission_classes = (IsAdminUser,)
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsAdminUser,)
    ordering_fields = '__all__'
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend)


class BasicViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_fields = '__all__'
    ordering_fields = '__all__'
    ordering = ('id',)
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend)


class FornecedorViewSet(BasicViewSet):
    queryset = Fornecedor.objects.all()
    serializer_class = FornecedorSerializer
    ordering = ('nome',)


class MaterialViewSet(BasicViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
    ordering = ('nome',)


class PlacaViewSet(BasicViewSet):
    queryset = Placa.objects.all()
    serializer_class = PlacaSerializer


class RecorteRetangularViewSet(BasicViewSet):
    queryset = RecorteRetangular.objects.all()
    serializer_class = RecorteRetangularSerializer


class RecorteTriangularViewSet(BasicViewSet):
    queryset = RecorteTriangular.objects.all()
    serializer_class = RecorteTriangularSerializer


class RecorteCircularViewSet(BasicViewSet):
    queryset = RecorteCircular.objects.all()
    serializer_class = RecorteCircularSerializer
