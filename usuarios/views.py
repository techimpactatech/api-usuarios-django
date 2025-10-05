from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Usuario
from .serializers import UsuarioSerializer
from .pagination import ZeroBasedPageNumberPagination

# ====== SCHEMAS p/ Swagger ======
USUARIO_SCHEMA = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "id":            openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
        "nome":          openapi.Schema(type=openapi.TYPE_STRING,  example="Ana Silva"),
        "email":         openapi.Schema(type=openapi.TYPE_STRING,  example="ana@exemplo.com"),
        "data_criacao":  openapi.Schema(type=openapi.TYPE_STRING,  format="date-time", example="2025-10-02T23:59:59Z"),
    },
)

PAGE_SCHEMA = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "content":       openapi.Schema(type=openapi.TYPE_ARRAY, items=USUARIO_SCHEMA),
        "page":          openapi.Schema(type=openapi.TYPE_INTEGER, example=0),
        "size":          openapi.Schema(type=openapi.TYPE_INTEGER, example=20),
        "totalElements": openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
        "totalPages":    openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
    },
    example={
        "content": [
            {"id": 1, "nome": "Ana Silva", "email": "ana@exemplo.com", "data_criacao": "2025-10-02T23:59:59Z"}
        ],
        "page": 0, "size": 20, "totalElements": 1, "totalPages": 1
    }
)

PROBLEM_400 = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "title":  openapi.Schema(type=openapi.TYPE_STRING,  example="Requisição inválida"),
        "status": openapi.Schema(type=openapi.TYPE_INTEGER, example=400),
        "detail": openapi.Schema(type=openapi.TYPE_STRING,  example="Dados inválidos"),
        "errors": openapi.Schema(type=openapi.TYPE_OBJECT, additional_properties=openapi.Schema(type=openapi.TYPE_STRING)),
    },
    example={
        "title": "Requisição inválida",
        "status": 400,
        "detail": "Dados inválidos",
        "errors": {"email": "deve ser um e-mail válido", "nome": "não deve estar em branco"}
    }
)

PROBLEM_404 = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "title":  openapi.Schema(type=openapi.TYPE_STRING,  example="Não encontrado"),
        "status": openapi.Schema(type=openapi.TYPE_INTEGER, example=404),
        "detail": openapi.Schema(type=openapi.TYPE_STRING,  example="Usuário não encontrado"),
    },
    example={"title": "Não encontrado", "status": 404, "detail": "Usuário não encontrado"}
)

PROBLEM_409 = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "title":  openapi.Schema(type=openapi.TYPE_STRING,  example="Conflito"),
        "status": openapi.Schema(type=openapi.TYPE_INTEGER, example=409),
        "detail": openapi.Schema(type=openapi.TYPE_STRING,  example="E-mail já cadastrado"),
    },
    example={"title": "Conflito", "status": 409, "detail": "E-mail já cadastrado"}
)

# ====== VIEWSET (sem PATCH) ======
class UsuarioViewSet(viewsets.ViewSet):
    """
    CRUD de Usuários (GET, POST, PUT, DELETE)
    """
    pagination_class = ZeroBasedPageNumberPagination  # só afeta list()

    @swagger_auto_schema(
        operation_summary="Listar usuários (paginado)",
        manual_parameters=[
            openapi.Parameter('page', openapi.IN_QUERY, description="Página (0-based)", type=openapi.TYPE_INTEGER, default=0),
            openapi.Parameter('size', openapi.IN_QUERY, description="Tamanho da página (1-100)", type=openapi.TYPE_INTEGER, default=20),
        ],
        responses={200: PAGE_SCHEMA}
    )
    def list(self, request):
        qs = Usuario.objects.all().order_by("id")
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(qs, request, view=self)
        data = UsuarioSerializer(page, many=True).data
        return paginator.get_paginated_response(data)

    @swagger_auto_schema(
        operation_summary="Obter usuário por ID",
        responses={200: USUARIO_SCHEMA, 404: PROBLEM_404}
    )
    def retrieve(self, request, pk=None):
        try:
            u = Usuario.objects.get(pk=pk)
        except Usuario.DoesNotExist:
            return Response({"title":"Não encontrado","status":404,"detail":"Usuário não encontrado"}, status=404)
        return Response(UsuarioSerializer(u).data)

    @swagger_auto_schema(
        operation_summary="Criar novo usuário",
        request_body=UsuarioSerializer,
        responses={201: USUARIO_SCHEMA, 400: PROBLEM_400, 409: PROBLEM_409}
    )
    def create(self, request):
        ser = UsuarioSerializer(data=request.data)
        if not ser.is_valid():
            return Response({"title":"Requisição inválida","status":400,"detail":"Dados inválidos","errors":ser.errors}, status=400)
        email = ser.validated_data.get("email")
        if Usuario.objects.filter(email=email).exists():
            return Response({"title":"Conflito","status":409,"detail":"E-mail já cadastrado"}, status=409)
        u = ser.save()
        return Response(UsuarioSerializer(u).data, status=201)

    @swagger_auto_schema(
        operation_summary="Atualizar usuário por ID",
        request_body=UsuarioSerializer,
        responses={200: USUARIO_SCHEMA, 400: PROBLEM_400, 404: PROBLEM_404, 409: PROBLEM_409}
    )
    def update(self, request, pk=None):
        try:
            u = Usuario.objects.get(pk=pk)
        except Usuario.DoesNotExist:
            return Response({"title":"Não encontrado","status":404,"detail":"Usuário não encontrado"}, status=404)
        ser = UsuarioSerializer(u, data=request.data, partial=False)
        if not ser.is_valid():
            return Response({"title":"Requisição inválida","status":400,"detail":"Dados inválidos","errors":ser.errors}, status=400)
        email = ser.validated_data.get("email")
        if Usuario.objects.filter(email=email).exclude(pk=pk).exists():
            return Response({"title":"Conflito","status":409,"detail":"E-mail já cadastrado"}, status=409)
        u = ser.save()
        return Response(UsuarioSerializer(u).data)

    @swagger_auto_schema(
        operation_summary="Remover usuário por ID",
        responses={204: 'No Content', 404: PROBLEM_404}
    )
    def destroy(self, request, pk=None):
        try:
            u = Usuario.objects.get(pk=pk)
        except Usuario.DoesNotExist:
            return Response({"title":"Não encontrado","status":404,"detail":"Usuário não encontrado"}, status=404)
        u.delete()
        return Response(status=204)