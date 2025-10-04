from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from django.db import IntegrityError, transaction
from .models import Usuario
from .serializers import UsuarioSerializer

class UsuarioViewSet(ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

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
