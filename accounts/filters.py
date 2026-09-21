import django_filters

from .models import Service


class ServiceFilter(django_filters.FilterSet):

    min_price = django_filters.NumberFilter(
        field_name="price",
        lookup_expr="gte"
    )

    max_price = django_filters.NumberFilter(
        field_name="price",
        lookup_expr="lte"
    )

    category = django_filters.UUIDFilter(
        field_name="category_id"
    )

    provider = django_filters.UUIDFilter(
        field_name="provider_id"
    )

    status = django_filters.CharFilter(
        field_name="status"
    )

    class Meta:
        model = Service
        fields = [
            "min_price",
            "max_price",
            "category",
            "provider",
            "status",
        ]