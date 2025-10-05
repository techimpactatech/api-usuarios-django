from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from usuarios.views import UsuarioViewSet

# Swagger (drf-yasg)
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny

schema_view = get_schema_view(
    openapi.Info(
        title="API de Usuários (Django)",
        default_version='v1',
        description="CRUD de usuários com paginação 0-based (page/size)",
    ),
    public=True,
    permission_classes=[AllowAny],
)

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet, basename='usuarios')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),                      # rotas /usuarios
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/'  , schema_view.with_ui('redoc',   cache_timeout=0), name='schema-redoc'),
]
