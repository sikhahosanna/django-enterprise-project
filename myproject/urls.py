"""
URL configuration for myproject project.
"""

from django.contrib import admin
from django.urls import include, path
from accounts.health import health_check, database_health, redis_health


from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)


urlpatterns = [
    path("admin/", admin.site.urls),

    path(
    "api/v1/",
    include("accounts.urls"),
),
    

    path(
        "api/schema/",
        SpectacularAPIView.as_view(),
        name="schema",
    ),

    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(
            url_name="schema",
        ),
        name="swagger-ui",
    ),

    path("api/health/", health_check, name="health"),
path("api/health/database/", database_health, name="health-database"),
path("api/health/redis/", redis_health, name="health-redis"),
]
