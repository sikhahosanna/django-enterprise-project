
from django.contrib import admin

from .models import (
    User,
    Profile,
    DriverProfile,
    VehicleType,
    Vehicle,
    RideStatus,
    Ride,
)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
    )

    search_fields = (
        "email",
        "first_name",
        "last_name",
    )

    list_filter = (
        "is_staff",
        "is_active",
    )

    ordering = (
        "email",
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "first_name",
        "last_name",
        "phone",
        "is_deleted",
    )

    search_fields = (
        "user__email",
        "first_name",
        "last_name",
        "phone",
    )

    list_filter = (
        "is_deleted",
    )

    ordering = (
        "first_name",
    )


@admin.register(DriverProfile)
class DriverProfileAdmin(admin.ModelAdmin):
    list_display = (
        "license_number",
        "user",
        "status",
        "created_at",
        "updated_at",
    )

    search_fields = (
        "license_number",
        "user__email",
    )

    list_filter = (
        "status",
    )

    ordering = (
        "-created_at",
    )


@admin.register(VehicleType)
class VehicleTypeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "created_at",
        "updated_at",
    )

    search_fields = (
        "name",
    )

    list_filter = (
        "name",
    )

    ordering = (
        "name",
    )


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = (
        "registration_number",
        "driver",
        "vehicle_type",
        "model",
        "created_at",
    )

    search_fields = (
        "registration_number",
        "model",
        "driver__license_number",
    )

    list_filter = (
        "vehicle_type",
    )

    ordering = (
        "-created_at",
    )


@admin.register(RideStatus)
class RideStatusAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "created_at",
        "updated_at",
    )

    search_fields = (
        "name",
    )

    list_filter = (
        "name",
    )

    ordering = (
        "name",
    )


@admin.register(Ride)
class RideAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "rider",
        "driver",
        "status",
        "fare",
        "created_at",
    )

    search_fields = (
        "rider__email",
        "driver__license_number",
        "pickup_address",
        "dropoff_address",
    )

    list_filter = (
        "status",
        "created_at",
    )

    ordering = (
        "-created_at",
    )
