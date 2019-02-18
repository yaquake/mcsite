import os
from celery.schedules import crontab

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'rgxi#(na8-p6-7rjs*z)g4$@2o0o!8qg9qit1s5mvydjtl(=##'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

FILE_UPLOAD_PERMISSIONS = 0o644

# Application definition

INSTALLED_APPS = [
    'admin_honeypot',
    'main.apps.MainConfig',
    'django_summernote',
    'easy_thumbnails',
    'celery',
    'jet.dashboard',
    'jet',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THUMBNAIL_ALIASES = {
    '': {
        'prop_image': {'size': (400, 300), 'crop': 'smart'},
        'personnel_image': {'size': (600, 800), 'crop': 'smart'},
        'news_image': {'size': (800, 500), 'crop': 'smart'},
    },
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mcsite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'main.context_processor.get_motto',
            ],
        },
    },
]

WSGI_APPLICATION = 'mcsite.wsgi.application'


# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'mcsite',
        'USER': 'postgres',
        'PASSWORD': 'uVbiho60',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Redis cache

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://localhost:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
        "KEY_PREFIX": "properties"
    }
}
CACHE_TTL = 60 * 15

# Celery settings

CELERY_BROKER_URL = 'redis://localhost'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Pacific/Auckland'
CELERY_IMPORTS = ['main.tasks', ]


CELERY_BEAT_SCHEDULE = {
 'update_from_xml': {
       'task': 'main.tasks.update_from_xml',
       'schedule': 7200,
    },

}


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Pacific/Auckland'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'mcsite/static')
]

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

SUMMERNOTE_THEME = 'bs4'


SUMMERNOTE_CONFIG = {
    'summernote': {
        'width': '100%',
        'height': '1200'
    },

}

GOOGLE_RECAPTCHA_SECRET_KEY = '6LcMGpIUfgdfgdfgdfgf8M0_fAPEhN4paamBY5yH_K8'

try:
    from .local_settings import *
except ImportError:
    pass

