"""
Django settings for myproject project.
"""

import os
from pathlib import Path
from datetime import timedelta

from dotenv import load_dotenv


# =========================================================
# BASE DIRECTORY
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

LOG_DIR = BASE_DIR / "logs"

LOG_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# =========================================================
# ENVIRONMENT
# =========================================================

load_dotenv(
    BASE_DIR / ".env"
)


# =========================================================
# SECURITY
# =========================================================

SECRET_KEY = os.getenv(
    "SECRET_KEY"
)

DEBUG = True

ALLOWED_HOSTS = []


# =========================================================
# APPLICATIONS
# =========================================================

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

    # API Documentation
    "drf_spectacular",
    "drf_spectacular_sidecar",

    # Filtering
    "django_filters",

    # JWT blacklist
    "rest_framework_simplejwt.token_blacklist",
]
ASGI_APPLICATION = "myproject.asgi.application"
ASGI_APPLICATION = "myproject.asgi.application"

# =========================================================
# CHANNEL LAYERS
# =========================================================

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    },
}
# =========================================================
# MIDDLEWARE
# =========================================================

MIDDLEWARE = [

    "django.middleware.security.SecurityMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",

    "django.middleware.common.CommonMiddleware",

    "django.middleware.csrf.CsrfViewMiddleware",

    "django.contrib.auth.middleware.AuthenticationMiddleware",

    "django.contrib.messages.middleware.MessageMiddleware",

    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# =========================================================
# URL CONFIGURATION
# =========================================================

ROOT_URLCONF = "myproject.urls"


# =========================================================
# TEMPLATES
# =========================================================

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


# =========================================================
# WSGI
# =========================================================

WSGI_APPLICATION = "myproject.wsgi.application"


# =========================================================
# DATABASE
# =========================================================

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


# =========================================================
# CUSTOM USER MODEL
# =========================================================

AUTH_USER_MODEL = "accounts.User"


# =========================================================
# PASSWORD VALIDATION
# =========================================================

AUTH_PASSWORD_VALIDATORS = [

    {
        "NAME":
            "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },

    {
        "NAME":
            "django.contrib.auth.password_validation.MinimumLengthValidator",
    },

    {
        "NAME":
            "django.contrib.auth.password_validation.CommonPasswordValidator",
    },

    {
        "NAME":
            "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]
# =========================================================
# JWT CONFIGURATION
# =========================================================
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}



# =========================================================
# REST FRAMEWORK
# =========================================================

REST_FRAMEWORK = {

    "DEFAULT_AUTHENTICATION_CLASSES": (

        "rest_framework_simplejwt.authentication.JWTAuthentication",

    ),

    "EXCEPTION_HANDLER":
        "accounts.utils.exceptions.custom_exception_handler",
    "DEFAULT_SCHEMA_CLASS":
        "drf_spectacular.openapi.AutoSchema",

    "DEFAULT_FILTER_BACKENDS": (

        "rest_framework.filters.SearchFilter",

        "rest_framework.filters.OrderingFilter",

        "django_filters.rest_framework.DjangoFilterBackend",

    ),

    "DEFAULT_PAGINATION_CLASS":
        "rest_framework.pagination.PageNumberPagination",

    "PAGE_SIZE": 5,
}


# =========================================================
# API DOCUMENTATION
# =========================================================

SPECTACULAR_SETTINGS = {

    "TITLE":
        "My Project API",

    "DESCRIPTION":
        "API Documentation",

    "VERSION":
        "1.0.0",
}


# =========================================================
# INTERNATIONALIZATION
# =========================================================

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# =========================================================
# STATIC FILES
# =========================================================

STATIC_URL = "static/"


# =========================================================
# MEDIA FILES
# =========================================================

MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR / "media"


# =========================================================
# RIDE FARE CONFIGURATION
# =========================================================
#
# Formula:
#
# Base Fare
#     +
# Distance Charge
#     +
# Time Charge
#     +
# Surge Charge
#     =
# Final Fare
#
# These values are configurable.
# Do not hardcode them inside views.
#


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


# =========================================================
# SURGE CONFIGURATION
# =========================================================
#
# 1.00 = No surge
# 1.25 = 25% surge
# 1.50 = 50% surge
# 2.00 = 100% surge
#

RIDE_SURGE_MULTIPLIER = 1.00


# =========================================================
# LOGGING
# =========================================================

LOGGING = {

    "version": 1,

    "disable_existing_loggers": False,

    "handlers": {

        "file": {

            "level": "ERROR",

            "class": "logging.FileHandler",

            "filename":
                str(LOG_DIR / "error.log"),
        },
    },

    "loggers": {

        "django": {

            "handlers": [
                "file"
            ],

            "level": "ERROR",

            "propagate": True,
        },

        "accounts": {

            "handlers": [
                "file"
            ],

            "level": "ERROR",

            "propagate": False,
        },
    },
}