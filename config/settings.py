from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'dev-only'
DEBUG = True
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin','django.contrib.auth','django.contrib.contenttypes',
    'django.contrib.sessions','django.contrib.messages','django.contrib.staticfiles',
    'rest_framework', 'drf_spectacular','drf_yasg',
    'usuarios',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'

# >>> Postgres (porta 5433)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'tcc_framework',
        'USER': 'tcc_user',
        'PASSWORD': 'tcc_pass',
        'HOST': 'localhost',
        'PORT': '5433',
    }
}

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True
STATIC_URL = 'static/'

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_RENDERER_CLASSES': ['rest_framework.renderers.JSONRenderer'],
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'API de Usuários (Django)',
    'DESCRIPTION': 'CRUD de usuários para comparativo de frameworks',
    'VERSION': 'v1.0',
    'SERVERS': [{'url': 'http://127.0.0.1:8000', 'description': 'Local'}],
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST': True,
    'SECURITY': [],
}
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],              # pode deixar vazio
        'APP_DIRS': True,        # precisa ser True pro admin achar os templates
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'usuarios.pagination.ZeroBasedPageNumberPagination',
    'PAGE_SIZE': 20,
}
