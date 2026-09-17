from django.db import connection
from django.core.cache import cache
from django.http import JsonResponse


def health_check(request):
    return JsonResponse({
        "status": "healthy"
    })


def database_health(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")

        return JsonResponse({
            "status": "healthy",
            "database": "healthy"
        })

    except Exception:
        return JsonResponse({
            "status": "unhealthy",
            "database": "unhealthy"
        }, status=503)


def redis_health(request):
    try:
        cache.set("health_check", "ok", 10)
        value = cache.get("health_check")

        if value == "ok":
            return JsonResponse({
                "status": "healthy",
                "redis": "healthy"
            })

        return JsonResponse({
            "status": "unhealthy",
            "redis": "unhealthy"
        }, status=503)

    except Exception:
        return JsonResponse({
            "status": "unhealthy",
            "redis": "unhealthy"
        }, status=503)