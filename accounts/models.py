import uuid

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


# =========================================================
# USER MANAGER
# =========================================================

class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):

        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)

        user = self.model(
            email=email,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(
            email,
            password,
            **extra_fields
        )


# =========================================================
# USER
# =========================================================

class User(AbstractUser):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    email = models.EmailField(
        unique=True
    )

    username = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


# =========================================================
# PROFILE
# =========================================================

class Profile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    first_name = models.CharField(
        max_length=100
    )

    last_name = models.CharField(
        max_length=100
    )

    phone = models.CharField(
        max_length=15
    )

    profile_image = models.ImageField(
        upload_to="profile_images/",
        null=True,
        blank=True
    )

    is_deleted = models.BooleanField(
        default=False
    )

    def __str__(self):
        return self.user.email


# =========================================================
# DRIVER PROFILE
# =========================================================

class DriverProfile(models.Model):

    class DriverStatus(models.TextChoices):

        ACTIVE = "active", "Active"
        INACTIVE = "inactive", "Inactive"
        SUSPENDED = "suspended", "Suspended"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="driver_profile"
    )

    license_number = models.CharField(
        max_length=50,
        unique=True
    )

    status = models.CharField(
        max_length=20,
        choices=DriverStatus.choices,
        default=DriverStatus.INACTIVE
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        indexes = [
            models.Index(
                fields=["status"]
            ),
        ]

    def __str__(self):
        return self.license_number


# =========================================================
# VEHICLE TYPE
# =========================================================

class VehicleType(models.Model):

    class Type(models.TextChoices):

        BIKE = "bike", "Bike"
        AUTO = "auto", "Auto"
        CAR = "car", "Car"
        SUV = "suv", "SUV"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    name = models.CharField(
        max_length=20,
        choices=Type.choices,
        unique=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        indexes = [
            models.Index(
                fields=["name"]
            ),
        ]

    def __str__(self):
        return self.name


# =========================================================
# VEHICLE
# =========================================================

class Vehicle(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    driver = models.ForeignKey(
        DriverProfile,
        on_delete=models.CASCADE,
        related_name="vehicles"
    )

    vehicle_type = models.ForeignKey(
        VehicleType,
        on_delete=models.PROTECT,
        related_name="vehicles"
    )

    registration_number = models.CharField(
        max_length=20,
        unique=True
    )

    model = models.CharField(
        max_length=100
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        indexes = [
            models.Index(
                fields=["driver"]
            ),
            models.Index(
                fields=["vehicle_type"]
            ),
        ]

    def __str__(self):
        return self.registration_number


# =========================================================
# RIDE STATUS
# =========================================================

class RideStatus(models.Model):

    class Status(models.TextChoices):

        REQUESTED = "requested", "Requested"
        ACCEPTED = "accepted", "Accepted"
        DRIVER_ARRIVING = "driver_arriving", "Driver Arriving"
        STARTED = "started", "Started"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    name = models.CharField(
        max_length=30,
        choices=Status.choices,
        unique=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        indexes = [
            models.Index(
                fields=["name"]
            ),
        ]

    def __str__(self):
        return self.name


# =========================================================
# RIDE
# =========================================================

class Ride(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    rider = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="rides"
    )

    driver = models.ForeignKey(
        DriverProfile,
        on_delete=models.PROTECT,
        related_name="rides",
        null=True,
        blank=True
    )

    vehicle_type = models.ForeignKey(
        VehicleType,
        on_delete=models.PROTECT,
        related_name="rides",
        null=True,
        blank=True
    )

    status = models.ForeignKey(
        RideStatus,
        on_delete=models.PROTECT,
        related_name="rides"
    )

    pickup_address = models.CharField(
        max_length=255
    )

    pickup_latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6
    )

    pickup_longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6
    )

    dropoff_address = models.CharField(
        max_length=255
    )

    dropoff_latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6
    )

    dropoff_longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6
    )

    fare = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:

        indexes = [
            models.Index(
                fields=["rider"]
            ),
            models.Index(
                fields=["driver"]
            ),
            models.Index(
                fields=["status"]
            ),
            models.Index(
                fields=["created_at"]
            ),

            # Task 2 performance indexes
            models.Index(
                fields=["rider", "created_at"]
            ),
            models.Index(
                fields=["driver", "created_at"]
            ),
            models.Index(
                fields=["status", "created_at"]
            ),
        ]

        constraints = [
            models.CheckConstraint(
                condition=models.Q(
                    fare__gte=0
                ),
                name="ride_fare_non_negative"
            ),
        ]

    def __str__(self):
        return str(self.id)