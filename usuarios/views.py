from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from django.db import IntegrityError, transaction
from .models import Usuario
from .serializers import UsuarioSerializer

from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse
from .openapi import RESP_BAD_REQUEST, RESP_NOT_FOUND, RESP_CONFLICT

@extend_schema_view(
    list=extend_schema(summary="Listar usuários", tags=["Usuários"], responses={200: UsuarioSerializer}),
    retrieve=extend_schema(summary="Obter usuário por ID", tags=["Usuários"], responses={200: UsuarioSerializer, 404: RESP_NOT_FOUND}),
    create=extend_schema(summary="Criar novo usuário", tags=["Usuários"], responses={201: UsuarioSerializer, 400: RESP_BAD_REQUEST, 409: RESP_CONFLICT}),
    update=extend_schema(summary="Atualizar usuário por ID", tags=["Usuários"], responses={200: UsuarioSerializer, 400: RESP_BAD_REQUEST, 404: RESP_NOT_FOUND, 409: RESP_CONFLICT}),
    destroy=extend_schema(summary="Remover usuário por ID", tags=["Usuários"], responses={204: OpenApiResponse(description="Removido com sucesso"), 404: RESP_NOT_FOUND}),
)

class UsuarioViewSet(ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    http_method_names = ['get', 'post', 'put', 'delete', 'head', 'options']

def create(self, request, *args, **kwargs):
    ser = self.get_serializer(data=request.data)
    ser.is_valid(raise_exception=True)
    try:
        with transaction.atomic():
            self.perform_create(ser)
    except IntegrityError:
        return Response(
            {"type":"about:blank","title":"Conflito","status":409,"detail":"email já cadastrado"},
            status=status.HTTP_409_CONFLICT
        )
    ser.instance.refresh_from_db()
    headers = self.get_success_headers(ser.data)
    return Response(ser.data, status=status.HTTP_201_CREATED, headers=headers)

def update(self, request, *args, **kwargs):
        instance = self.get_object()
        ser = self.get_serializer(instance, data=request.data)
        ser.is_valid(raise_exception=True)
        try:
            with transaction.atomic():
                self.perform_update(ser)
        except IntegrityError:
            return Response(
                {"type":"about:blank","title":"Conflito","status":409,"detail":"email já cadastrado"},
                status=status.HTTP_409_CONFLICT
            )
        return Response(ser.data, status=status.HTTP_200_OK)

    # 🚫 Desabilita o PATCH
def partial_update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)