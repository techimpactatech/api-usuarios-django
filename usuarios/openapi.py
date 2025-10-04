from drf_spectacular.utils import (
    OpenApiExample, OpenApiResponse, inline_serializer
)
from rest_framework import serializers

# Schema "problem+json" como serializer inline (compatível com versões antigas)
ProblemDetailSerializer = inline_serializer(
    name='ProblemDetail',
    fields={
        'type': serializers.CharField(required=False),
        'title': serializers.CharField(),
        'status': serializers.IntegerField(),
        'detail': serializers.CharField(),
        'instance': serializers.CharField(required=False),
    }
)

BAD_REQUEST_EXAMPLE = OpenApiExample(
    'BadRequest',
    value={
        "title":"Requisição inválida",
        "status":400,
        "detail":"Dados inválidos",
        "errors":{"email":"deve ser um e-mail válido","nome":"não deve estar em branco"}
    },
    response_only=True
)

NOT_FOUND_EXAMPLE = OpenApiExample(
    'NotFound',
    value={"title":"Recurso não encontrado","status":404,"detail":"Usuário não encontrado"},
    response_only=True
)

CONFLICT_EXAMPLE = OpenApiExample(
    'Conflict',
    value={"title":"Conflito","status":409,"detail":"email já cadastrado"},
    response_only=True
)

RESP_BAD_REQUEST = OpenApiResponse(response=ProblemDetailSerializer, description='Dados inválidos', examples=[BAD_REQUEST_EXAMPLE])
RESP_NOT_FOUND  = OpenApiResponse(response=ProblemDetailSerializer, description='Recurso não encontrado', examples=[NOT_FOUND_EXAMPLE])
RESP_CONFLICT   = OpenApiResponse(response=ProblemDetailSerializer, description='Conflito (e-mail já cadastrado)', examples=[CONFLICT_EXAMPLE])
