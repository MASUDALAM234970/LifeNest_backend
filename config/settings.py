
"""
Django settings for config project.

"""

from pathlib import Path

from datetime import timedelta
from decouple import config
import os


BASE_DIR = Path(__file__).resolve().parent.parent




# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

#DEBUG = config('DEBUG', default=False, cast=bool)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1').split(',')

DEBUG = True

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    "192.168.0.103",
]



# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
      # Third party apps
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',  # For token blacklisting
    'corsheaders',
    'drf_spectacular',  # API documentation
    
    # Local apps
    'users.apps.UsersConfig',
    'mood_tracker.apps.MoodTrackerConfig',
    'music.apps.MusicConfig',
    'chatbot.apps.ChatbotConfig'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # CORS middleware (must be before CommonMiddleware)
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Custom User Model
AUTH_USER_MODEL = "users.User"
# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS' : {
             'min_length': 8,
        }
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




STATIC_URL = 'static/'



DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework Configuration
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.FormParser',
    ),

    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),

    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),

    'EXCEPTION_HANDLER': 'users.exceptions.custom_exception_handler',
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

# REST_FRAMEWORK = {
#     'DEFAULT_RENDERER_CLASSES': (
#         'rest_framework.renderers.JSONRenderer',
#     ),
#     'DEFAULT_PARSER_CLASSES': (
#         'rest_framework.parsers.JSONParser',
#         'rest_framework.parsers.MultiPartParser',
#         'rest_framework.parsers.FormParser',
#     ),
#     'EXCEPTION_HANDLER': 'users.exceptions.custom_exception_handler',
#     'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
#     'PAGE_SIZE': 20,
#     'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
# }




# Simple JWT Configuration
SIMPLE_JWT = {
    # Token lifetime
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
    
    # Token claims
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    
    # Token format
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    
    # Token classes
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    
    # Sliding tokens
    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(hours=1),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=7),
}



# CORS Configuration (Allow Flutter app to make requests)
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # For web testing
    "http://127.0.0.1:3000",
    # Add your Flutter app URLs here
]

# For development only - allow all origins
# CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]
# Email Configuration

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_HOST = config("EMAIL_HOST")
EMAIL_PORT = config("EMAIL_PORT", cast=int)
EMAIL_USE_TLS = config("EMAIL_USE_TLS", cast=bool)

EMAIL_HOST_USER = config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")

DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL")



# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
# EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
# EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
# EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
# EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
# DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default=EMAIL_HOST_USER)

# Firebase Configuration
FIREBASE_CREDENTIALS_PATH = config('FIREBASE_CREDENTIALS_PATH', default='firebase-credentials.json')

# Frontend URL (for email links)
FRONTEND_URL = config('FRONTEND_URL', default='http://localhost:3000')


# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default=EMAIL_HOST_USER)

# Firebase Configuration
FIREBASE_CREDENTIALS_PATH = config('FIREBASE_CREDENTIALS_PATH', default='firebase-credentials.json')

# Frontend URL (for email links)
FRONTEND_URL = config('FRONTEND_URL', default='http://localhost:3000')


# Celery Configuration (for async tasks)

CELERY_BROKER_URL = config('CELERY_BROKER_URL', default='redis://localhost:6379/0')
CELERY_RESULT_BACKEND = config('CELERY_RESULT_BACKEND', default='redis://localhost:6379/0')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE

# Security Settings for Production
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

# DRF Spectacular (API Documentation) Settings
SPECTACULAR_SETTINGS = {
    'TITLE': 'User Authentication API',
    'DESCRIPTION': 'API for user authentication with Firebase and JWT',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}

# Account Settings
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_EMAIL_REQUIRED = True
EMAIL_VERIFICATION_REQUIRED = True

# Token Expiry (for email verification and password reset)
EMAIL_VERIFICATION_TOKEN_EXPIRY_HOURS = 24
PASSWORD_RESET_TOKEN_EXPIRY_HOURS = 1