import mimetypes
import os
from pathlib import Path
import environ
from fakeredis import FakeConnection

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

env = environ.Env(
    DEBUG=(bool, False),
    DATABASE_TYPE=(str, 'pgsql'),
    DATABASE_USER=(str, 'postgres'),
    DATABASE_PASSWORD=(str, 'postgres'),
    DATABASE_HOST=(str, 'localhost'),
    DATABASE_PORT=(int, '5432'),
    DATABASE_NAME=(str, 'backend'),
    EMAIL_HOST=(str, ''),
    EMAIL_USER=(str, ''),
    EMAIL_PASSWORD=(str, ''),
    EMAIL_USE_TLS=(bool, False),
    EMAIL_USE_SSL=(bool, False),
    EMAIL_FROM=(str, ''),
    EMAIL_SMTP_PORT=(int, 25),
    REDIS_HOST=(str, 'localhost'),
    REDIS_PORT=(int, 6379),
    REDIS_DB=(int, 0),
    REDIS_PASSWORD=(str, ''),
    PAGE_CACHE_TIME=(int, 60),
)

environ.Env.read_env(os.path.join(BASE_DIR, '.env'))


if env('EMAIL_HOST') is not None and env('EMAIL_HOST') != '':
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = env('EMAIL_HOST')
    EMAIL_USER = env('EMAIL_USER')
    EMAIL_PASSWORD = env('EMAIL_PASSWORD')
    EMAIL_USE_TLS = env('EMAIL_USE_TLS')
    EMAIL_USE_SSL = env('EMAIL_USE_SSL')
    EMAIL_FROM = env('EMAIL_FROM') or env('EMAIL_USER')
    EMAIL_SMTP_PORT = env('EMAIL_SMTP_PORT')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-kxr)0+uz_9=jdz0elc)-cbmxc2k5@(*)=cym0#r$s&(x#qzy&p'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'api',
    'BlogApi',
    'corsheaders',
    'Images',
    'ProjectApi',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
]

CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:5173",
]


ROOT_URLCONF = 'SecCodeSmithBackend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'SecCodeSmithBackend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases


if env('DATABASE_TYPE') == 'pgsql':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': env('DATABASE_NAME'),
            'USER': env('DATABASE_USER'),
            'PASSWORD': env('DATABASE_PASSWORD'),
            'HOST': env('DATABASE_HOST'),
            'PORT': env('DATABASE_PORT'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": "redis://:Password@127.0.0.1:6379/1",
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"
STATIC_ROOT = BASE_DIR / "static"

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ]
}

mimetypes.add_type("image/webp", ".webp", True)
DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760