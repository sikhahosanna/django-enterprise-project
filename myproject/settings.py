"""
Django settings for myproject project.
"""

import os
from pathlib import Path
from datetime import timedelta
from kombu import Queue
from celery.schedules import crontab
from dotenv import load_dotenv



# BASE DIRECTORY


BASE_DIR = Path(__file__).resolve().parent.parent

LOG_DIR = BASE_DIR / "logs"

LOG_DIR.mkdir(
    parents=True,
    exist_ok=True
)



# ENVIRONMENT

load_dotenv(
    BASE_DIR / ".env"
)

# SECURITY


SECRET_KEY = os.getenv("SECRET_KEY")

DEBUG = os.getenv(
    "DEBUG",
    "False"
).lower() == "true"

ALLOWED_HOSTS = [
    host.strip()
    for host in os.getenv(
        "ALLOWED_HOSTS",
        "127.0.0.1,localhost"
    ).split(",")
    if host.strip()
]

ASGI_APPLICATION = "myproject.asgi.application"



# CHANNEL LAYERS


CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    },
}


# APPLICATIONS


INSTALLED_APPS = [

    "daphne",

    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Project apps
    "core",
    "accounts",
    "common",
    "channels",

   
    

    # REST Framework
    "rest_framework",
    'django_celery_beat',

    # API Documentation
    "drf_spectacular",
    "drf_spectacular_sidecar",

    # Filtering
    "django_filters",

    # JWT blacklist
    "rest_framework_simplejwt.token_blacklist",

    # CORS
    "corsheaders",
]



# MIDDLEWARE


MIDDLEWARE = [

    "django.middleware.security.SecurityMiddleware",

    # CORS should be placed before CommonMiddleware
    "corsheaders.middleware.CorsMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",

    "django.middleware.common.CommonMiddleware",

    "django.middleware.csrf.CsrfViewMiddleware",

    "django.contrib.auth.middleware.AuthenticationMiddleware",

    "django.contrib.messages.middleware.MessageMiddleware",

    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.security.SecurityMiddleware",
   

]



# SECURITY SETTINGS


# Redirect HTTP to HTTPS in production
SECURE_SSL_REDIRECT = os.getenv(
    "SECURE_SSL_REDIRECT",
    "False"
).lower() == "true"


# Secure session cookie
SESSION_COOKIE_SECURE = os.getenv(
    "SESSION_COOKIE_SECURE",
    "False"
).lower() == "true"


# Secure CSRF cookie
CSRF_COOKIE_SECURE = os.getenv(
    "CSRF_COOKIE_SECURE",
    "False"
).lower() == "true"


# Prevent JavaScript from accessing session cookie
SESSION_COOKIE_HTTPONLY = True


# HSTS
SECURE_HSTS_SECONDS = int(
    os.getenv(
        "SECURE_HSTS_SECONDS",
        "0"
    )
)

SECURE_HSTS_INCLUDE_SUBDOMAINS = os.getenv(
    "SECURE_HSTS_INCLUDE_SUBDOMAINS",
    "False"
).lower() == "true"

SECURE_HSTS_PRELOAD = os.getenv(
    "SECURE_HSTS_PRELOAD",
    "False"
).lower() == "true"


# Prevent MIME type sniffing
SECURE_CONTENT_TYPE_NOSNIFF = True


# Prevent clickjacking
X_FRAME_OPTIONS = "DENY"



# CORS SETTINGS


CORS_ALLOWED_ORIGINS = [
    origin.strip()
    for origin in os.getenv(
        "CORS_ALLOWED_ORIGINS",
        ""
    ).split(",")
    if origin.strip()
]

# CSRF SETTINGS


CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.getenv(
        "CSRF_TRUSTED_ORIGINS",
        ""
    ).split(",")
    if origin.strip()
]


# URL CONFIGURATION


ROOT_URLCONF = "myproject.urls"

# TEMPLATES


TEMPLATES = [
    {
        "BACKEND":
            "django.template.backends.django.DjangoTemplates",

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

# WSGI


WSGI_APPLICATION = "myproject.wsgi.application"


# DATABASE


DATABASES = {
    "default": {
        "ENGINE":
            "django.db.backends.postgresql",

        "NAME":
            os.getenv("DB_NAME"),

        "USER":
            os.getenv("DB_USER"),

        "PASSWORD":
            os.getenv("DB_PASSWORD"),

        "HOST":
            os.getenv("DB_HOST"),

        "PORT":
            os.getenv("DB_PORT"),
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



# JWT CONFIGURATION


SIMPLE_JWT = {

    "ACCESS_TOKEN_LIFETIME": timedelta(
        minutes=30
    ),

    "REFRESH_TOKEN_LIFETIME": timedelta(
        days=1
    ),
}
# CELERY QUEUES

CELERY_TASK_QUEUES = (
    Queue("notifications"),
    Queue("reports"),
    Queue("maintenance"),
)

CELERY_TASK_DEFAULT_QUEUE = "notifications"
# CELERY BEAT SCHEDULE

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

    # RATE LIMITING / THROTTLING
    "DEFAULT_THROTTLE_CLASSES": [
        "accounts.throttles.AnonymousRateThrottle",
        "accounts.throttles.AuthenticatedRateThrottle",
    ],

    "DEFAULT_THROTTLE_RATES": {
        "anonymous": "20/minute",
        "authenticated": "100/minute",
        "login": "5/minute",
        "ride_creation": "10/minute",
        "sensitive": "5/minute",
    },
}

# API DOCUMENTATION


SPECTACULAR_SETTINGS = {

    "TITLE":
        "My Project API",

    "DESCRIPTION":
        "API Documentation",

    "VERSION":
        "1.0.0",
}


# INTERNATIONALIZATION


LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# STATIC FILES


STATIC_URL = "static/"



# MEDIA FILES


MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR / "media"



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



# SURGE CONFIGURATION


RIDE_SURGE_MULTIPLIER = 1.00


# LOGGING

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,

    "formatters": {
        "standard": {
            "format": "{asctime} | {levelname} | {name} | {message}",
            "style": "{",
        },
    },

    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },

        "file": {
            "class": "logging.FileHandler",
            "filename": str(LOG_DIR / "error.log"),
            "formatter": "standard",
        },
    },

    "loggers": {

        # 1. Application
        "application": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False,
        },

        # 2. Authentication
        "authentication": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False,
        },

        # 3. API
        "api": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False,
        },

        # 4. Database
        "database": {
            "handlers": ["console", "file"],
            "level": "WARNING",
            "propagate": False,
        },

        # 5. Celery
        "celery": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False,
        },

        # 6. WebSocket
        "websocket": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False,
        },

        # 7. Security
        "security": {
            "handlers": ["console", "file"],
            "level": "WARNING",
            "propagate": False,
        },

        # Django
        "django": {
            "handlers": ["console", "file"],
            "level": "ERROR",
            "propagate": False,
        },
    },
}