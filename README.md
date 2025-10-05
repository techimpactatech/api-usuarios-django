🟢 api-usuarios-django — Django REST Framework (Python)
📌 Descrição

CRUD de Usuários com DRF, paginação 0-based (?page&size) retornando {content,page,size,totalElements,totalPages}, erros padronizados e Swagger (drf-yasg).

✅ Pré-requisitos

Python 3.10+

pip

Docker (para Postgres)

Postgres local (ou container abaixo)

🐘 Banco de dados (Docker)

(use o mesmo container do Spring, se já estiver rodando)

docker run --name tcc-postgres ^
-e POSTGRES_DB=tcc_framework ^
-e POSTGRES_USER=tcc_user ^
-e POSTGRES_PASSWORD=tcc_pass ^
-p 5433:5432 ^
-v tcc_data:/var/lib/postgresql/data ^
-d postgres:15

▶️ Ambiente e dependências
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
# se não tiver requirements.txt:
# pip install django djangorestframework drf-yasg psycopg2-binary

⚙️ Configuração do banco (exemplo)

config/settings.py

DATABASES = {
  "default": {
    "ENGINE": "django.db.backends.postgresql",
    "NAME": "tcc_framework",
    "USER": "tcc_user",
    "PASSWORD": "tcc_pass",
    "HOST": "localhost",
    "PORT": "5433",
  }
}

INSTALLED_APPS = [
  # ...
  "rest_framework",
  "drf_yasg",
  "usuarios",
]

# (Opcional: deixar a paginação 0-based como padrão do projeto)
# REST_FRAMEWORK = {
#   "DEFAULT_PAGINATION_CLASS": "usuarios.pagination.ZeroBasedPageNumberPagination",
#   "PAGE_SIZE": 20,
# }

▶️ Migrar e rodar
python manage.py migrate
python manage.py runserver 8000

🔗 Endpoints

Swagger: http://127.0.0.1:8000/swagger/

Listar paginado: GET /usuarios/?page=0&size=20

Demais: POST /usuarios/, GET /usuarios/{id}/, PUT /usuarios/{id}/, DELETE /usuarios/{id}/

📦 Arquivos relevantes (resumo)
usuarios/models.py         # mapeamento da tabela existente
usuarios/serializers.py    # UsuarioSerializer
usuarios/pagination.py     # ZeroBasedPageNumberPagination (page/size 0-based)
usuarios/views.py          # UsuarioViewSet (GET/POST/PUT/DELETE) + schemas Swagger
config/urls.py             # router + swagger (schema_view)
