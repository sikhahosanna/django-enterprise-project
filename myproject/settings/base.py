"""
Base settings for myproject.
Common settings shared by all environments.
"""

import os
from pathlib import Path
from datetime import timedelta

from dotenv import load_dotenv
from kombu import Queue


# BASE DIRECTORY

BASE_DIR = Path(__file__).resolve().parent.parent.parent

load_dotenv(BASE_DIR / ".env")


# SECURITY

SECRET_KEY = os.getenv("SECRET_KEY")

DEBUG = os.getenv("DEBUG", "False").lower() == "true"

ALLOWED_HOSTS = [
    host.strip()
    for host in os.getenv(
        "ALLOWED_HOSTS",
        "127.0.0.1,localhost"
    ).split(",")
    if host.strip()
]

ASGI_APPLICATION = "myproject.asgi.application"
WSGI_APPLICATION = "myproject.wsgi.application"


# APPLICATIONS

INSTALLED_APPS = [
    "daphne",

    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "core",
    "accounts",
    "common",
    "channels",

    "rest_framework",
    "django_celery_beat",

    "drf_spectacular",
    "drf_spectacular_sidecar",

    "django_filters",

    "rest_framework_simplejwt.token_blacklist",

    "corsheaders",
]


# MIDDLEWARE

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# URL CONFIGURATION

ROOT_URLCONF = "myproject.urls"


# TEMPLATES

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# DATABASE

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT"),
    }
}


# CHANNEL LAYERS

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    },
}


# CELERY

CELERY_BROKER_URL = os.getenv(
    "CELERY_BROKER_URL",
    "redis://127.0.0.1:6379/0"
)

CELERY_RESULT_BACKEND = os.getenv(
    "CELERY_RESULT_BACKEND",
    "redis://127.0.0.1:6379/1"
)

CELERY_TASK_QUEUES = (
    Queue("notifications"),
    Queue("reports"),
    Queue("maintenance"),
)

CELERY_TASK_DEFAULT_QUEUE = "notifications"


# CELERY BEAT

CELERY_BEAT_SCHEDULE = {
    "clean-expired-data-daily": {
        "task": "accounts.tasks.clean_expired_data",
        "schedule": 60.0,
        "options": {"queue": "maintenance"},
    },
    "generate-daily-ride-summary": {
        "task": "accounts.tasks.generate_ride_report",
        "schedule": 60.0,
        "options": {"queue": "reports"},
    },
    "clean-old-temporary-data-daily": {
        "task": "accounts.tasks.process_background_records",
        "schedule": 60.0,
        "options": {"queue": "maintenance"},
    },
}


# REDIS CACHE

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.getenv(
            "REDIS_CACHE_URL",
            "redis://127.0.0.1:6379/1"
        ),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}


# CUSTOM USER MODEL

AUTH_USER_MODEL = "accounts.User"


# PASSWORD VALIDATION

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "MinimumLengthValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "CommonPasswordValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "NumericPasswordValidator"
        ),
    },
]


# JWT

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(
        minutes=int(
            os.getenv("JWT_ACCESS_TOKEN_MINUTES", "30")
        )
    ),
    "REFRESH_TOKEN_LIFETIME": timedelta(
        days=int(
            os.getenv("JWT_REFRESH_TOKEN_DAYS", "1")
        )
    ),
}


# REST FRAMEWORK

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS":
        "drf_spectacular.openapi.AutoSchema",

    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],

    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],

    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
    ],

    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],

    "DEFAULT_THROTTLE_RATES": {
        "anon": "1000/minute",
        "user": "1000/minute",
        "login": "20/minute",
        "ride_creation": "20/minute",
    },
}


# API DOCUMENTATION

SPECTACULAR_SETTINGS = {
    "TITLE": "My Project API",
    "DESCRIPTION": "API Documentation",
    "VERSION": "1.0.0",
}


# INTERNATIONALIZATION

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# CORS

CORS_ALLOWED_ORIGINS = [
    origin.strip()
    for origin in os.getenv(
        "CORS_ALLOWED_ORIGINS",
        ""
    ).split(",")
    if origin.strip()
]


# CSRF

CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.getenv(
        "CSRF_TRUSTED_ORIGINS",
        ""
    ).split(",")
    if origin.strip()
]


# SECURITY SETTINGS

SECURE_SSL_REDIRECT = os.getenv(
    "SECURE_SSL_REDIRECT",
    "False"
).lower() == "true"

SESSION_COOKIE_SECURE = os.getenv(
    "SESSION_COOKIE_SECURE",
    "False"
).lower() == "true"

CSRF_COOKIE_SECURE = os.getenv(
    "CSRF_COOKIE_SECURE",
    "False"
).lower() == "true"

SESSION_COOKIE_HTTPONLY = True

SECURE_HSTS_SECONDS = int(
    os.getenv("SECURE_HSTS_SECONDS", "0")
)

SECURE_HSTS_INCLUDE_SUBDOMAINS = os.getenv(
    "SECURE_HSTS_INCLUDE_SUBDOMAINS",
    "False"
).lower() == "true"

SECURE_HSTS_PRELOAD = os.getenv(
    "SECURE_HSTS_PRELOAD",
    "False"
).lower() == "true"

SECURE_CONTENT_TYPE_NOSNIFF = True

X_FRAME_OPTIONS = "DENY"


# EMAIL

EMAIL_BACKEND = os.getenv(
    "EMAIL_BACKEND",
    "django.core.mail.backends.console.EmailBackend"
)

EMAIL_HOST = os.getenv("EMAIL_HOST", "")

EMAIL_PORT = int(
    os.getenv("EMAIL_PORT", "587")
)

EMAIL_HOST_USER = os.getenv(
    "EMAIL_HOST_USER",
    ""
)

EMAIL_HOST_PASSWORD = os.getenv(
    "EMAIL_HOST_PASSWORD",
    ""
)

EMAIL_USE_TLS = os.getenv(
    "EMAIL_USE_TLS",
    "True"
).lower() == "true"


# STATIC FILES

STATIC_URL = "static/"

STATIC_ROOT = BASE_DIR / os.getenv(
    "STATIC_ROOT",
    "staticfiles"
)


# MEDIA FILES

MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR / os.getenv(
    "MEDIA_ROOT",
    "media"
)


# RIDE FARE CONFIGURATION

RIDE_FARE_CONFIG = {
    "bike": {
        "base_fare": 30,
        "per_km": 10,
        "per_minute": 2,
    },
    "auto": {
        "base_fare": 40,
        "per_km": 15,
        "per_minute": 3,
    },
    "car": {
        "base_fare": 60,
        "per_km": 20,
        "per_minute": 4,
    },
    "suv": {
        "base_fare": 80,
        "per_km": 25,
        "per_minute": 5,
    },
}


# SURGE

RIDE_SURGE_MULTIPLIER = 1.00


# LOGGING

LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(
    parents=True,
    exist_ok=True
)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,

    "formatters": {
        "verbose": {
            "format": "{asctime} {levelname} {name} {message}",
            "style": "{",
        },
    },

    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },

        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": str(LOG_DIR / "django.log"),
            "formatter": "verbose",
        },

        "error_file": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "filename": str(LOG_DIR / "error.log"),
            "formatter": "verbose",
        },
    },

    "loggers": {
        "django": {
            "handlers": [
                "console",
                "file",
                "error_file",
            ],
            "level": "INFO",
            "propagate": False,
        },

        "accounts": {
            "handlers": [
                "console",
                "file",
                "error_file",
            ],
            "level": "INFO",
            "propagate": False,
        },

        "celery": {
            "handlers": [
                "console",
                "file",
                "error_file",
            ],
            "level": "INFO",
            "propagate": False,
        },

        "channels": {
            "handlers": [
                "console",
                "file",
                "error_file",
            ],
            "level": "INFO",
            "propagate": False,
        },
    },
}