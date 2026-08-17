import re

from rest_framework import serializers

from django.core.validators import FileExtensionValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from django.db import transaction

from .models import (
    User,
    Profile,
    DriverProfile,
    Vehicle,
    VehicleType,
    Ride,
    RideStatus,
)

from .services.fare_service import (
    FareService,
)
from .utils.responses import (
    success_response,
    error_response,
)


# =========================================================
# REGISTER SERIALIZER
# =========================================================

class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        validators=[validate_password]
    )

    class Meta:

        model = User

        fields = [
            "email",
            "password",
        ]

    def validate_email(self, value):

        value = value.strip().lower()

        if User.objects.filter(
            email__iexact=value
        ).exists():

            raise serializers.ValidationError(
                "Email already exists."
            )

        return value

    def create(self, validated_data):

        return User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
        )


# =========================================================
# LOGIN SERIALIZER
# =========================================================

class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField()

    password = serializers.CharField(
        write_only=True
    )

    def validate(self, data):

        email = data["email"].strip().lower()

        user = authenticate(
            email=email,
            password=data["password"]
        )

        if not user:

            raise serializers.ValidationError(
                "Invalid email or password."
            )

        if not user.is_active:

            raise serializers.ValidationError(
                "User account is inactive."
            )

        data["user"] = user

        return data


# =========================================================
# CHANGE PASSWORD SERIALIZER
# =========================================================

class ChangePasswordSerializer(serializers.Serializer):

    current_password = serializers.CharField(
        write_only=True
    )

    new_password = serializers.CharField(
        write_only=True,
        validators=[validate_password]
    )

    def validate(self, data):

        user = self.context["request"].user

        if not user.check_password(
            data["current_password"]
        ):

            raise serializers.ValidationError(
                "Current password is incorrect."
            )

        if (
            data["current_password"]
            == data["new_password"]
        ):

            raise serializers.ValidationError({
                "new_password":
                    "New password must be different "
                    "from current password."
            })

        return data


# =========================================================
# PROFILE SERIALIZER
# =========================================================

class ProfileSerializer(serializers.ModelSerializer):

    profile_image = serializers.ImageField(
        required=False,
        validators=[
            FileExtensionValidator(
                allowed_extensions=[
                    "jpg",
                    "jpeg",
                    "png",
                ]
            )
        ]
    )

    class Meta:

        model = Profile

        fields = "__all__"

        read_only_fields = [
            "user",
        ]

    def validate_phone(self, value):

        value = value.strip()

        if not re.fullmatch(
            r"[0-9]{10}",
            value
        ):

            raise serializers.ValidationError(
                "Phone number must be 10 digits."
            )

        return value

    def validate_profile_image(self, image):

        if image.size > 5 * 1024 * 1024:

            raise serializers.ValidationError(
                "Image size should be less than 5MB."
            )

        return image


# =========================================================
# DRIVER SERIALIZER
# =========================================================

class DriverSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(
        write_only=True
    )

    password = serializers.CharField(
        write_only=True,
        validators=[validate_password]
    )

    first_name = serializers.CharField(
        write_only=True
    )

    last_name = serializers.CharField(
        write_only=True
    )

    phone = serializers.CharField(
        write_only=True
    )

    class Meta:

        model = DriverProfile

        fields = [
            "id",
            "email",
            "password",
            "first_name",
            "last_name",
            "phone",
            "license_number",
            "status",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
            "status",
        ]

    def validate_email(self, value):

        value = value.strip().lower()

        if User.objects.filter(
            email__iexact=value
        ).exists():

            raise serializers.ValidationError(
                "Email already exists."
            )

        return value

    def validate_phone(self, value):

        value = value.strip()

        if not re.fullmatch(
            r"[0-9]{10}",
            value
        ):

            raise serializers.ValidationError(
                "Phone number must be 10 digits."
            )

        return value

    @transaction.atomic
    def create(self, validated_data):

        email = validated_data.pop("email")
        password = validated_data.pop("password")

        first_name = validated_data.pop("first_name")
        last_name = validated_data.pop("last_name")
        phone = validated_data.pop("phone")

        validated_data.pop("status", None)

        user = User.objects.create_user(
            email=email,
            password=password
        )

        Profile.objects.create(
            user=user,
            first_name=first_name,
            last_name=last_name,
            phone=phone
        )

        driver = DriverProfile.objects.create(
            user=user,
            status=DriverProfile.DriverStatus.INACTIVE,
            **validated_data
        )

        return driver


# =========================================================
# VEHICLE SERIALIZER
# =========================================================

class VehicleSerializer(serializers.ModelSerializer):

    driver = serializers.PrimaryKeyRelatedField(
        queryset=DriverProfile.objects.all(),
        required=True
    )

    vehicle_type = serializers.PrimaryKeyRelatedField(
        queryset=VehicleType.objects.all(),
        required=True
    )

    class Meta:

        model = Vehicle

        fields = [
            "id",
            "driver",
            "vehicle_type",
            "registration_number",
            "model",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]

    def validate_registration_number(self, value):

        value = value.strip().upper()

        if not re.fullmatch(
            r"[A-Z]{2}[0-9]{2}[A-Z]{1,2}[0-9]{4}",
            value
        ):

            raise serializers.ValidationError(
                "Invalid vehicle registration number."
            )

        queryset = Vehicle.objects.filter(
            registration_number=value
        )

        if self.instance:

            queryset = queryset.exclude(
                pk=self.instance.pk
            )

        if queryset.exists():

            raise serializers.ValidationError(
                "Vehicle with this registration number "
                "already exists."
            )

        return value

    def validate_driver(self, value):

        if not value:

            raise serializers.ValidationError(
                "Driver is required."
            )

        return value

    def validate_vehicle_type(self, value):

        if not value:

            raise serializers.ValidationError(
                "Vehicle type is required."
            )

        return value


# =========================================================
# VEHICLE NESTED SERIALIZER
# =========================================================

class VehicleNestedSerializer(
    serializers.ModelSerializer
):

    type = serializers.CharField(
        source="vehicle_type.name",
        read_only=True
    )

    class Meta:

        model = Vehicle

        fields = [
            "type",
            "registration_number",
        ]


# =========================================================
# DRIVER NESTED SERIALIZER
# =========================================================

class DriverNestedSerializer(
    serializers.ModelSerializer
):

    name = serializers.SerializerMethodField()

    vehicle = serializers.SerializerMethodField()

    class Meta:

        model = DriverProfile

        fields = [
            "id",
            "name",
            "vehicle",
        ]

    def get_name(self, obj):

        try:

            profile = obj.user.profile

            return (
                f"{profile.first_name} "
                f"{profile.last_name}"
            ).strip()

        except Profile.DoesNotExist:

            return ""

    def get_vehicle(self, obj):

        vehicle = (
            Vehicle.objects
            .select_related("vehicle_type")
            .filter(driver=obj)
            .first()
        )

        if not vehicle:

            return None

        return VehicleNestedSerializer(
            vehicle
        ).data


# =========================================================
# RIDE CREATE SERIALIZER
# =========================================================

class RideCreateSerializer(
    serializers.ModelSerializer
):

    vehicle_type = serializers.PrimaryKeyRelatedField(
        queryset=VehicleType.objects.all(),
        required=True
    )

    status = serializers.CharField(
        source="status.name",
        read_only=True
    )

    class Meta:

        model = Ride

        fields = [
            "id",

            "pickup_address",
            "pickup_latitude",
            "pickup_longitude",

            "dropoff_address",
            "dropoff_latitude",
            "dropoff_longitude",

            "vehicle_type",

            "fare",

            "status",

            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "fare",
            "status",
            "created_at",
            "updated_at",
        ]

    # =====================================================
    # ADDRESS VALIDATION
    # =====================================================

    def validate_pickup_address(self, value):

        value = value.strip()

        if not value:

            raise serializers.ValidationError(
                "Pickup location is required."
            )

        return value

    def validate_dropoff_address(self, value):

        value = value.strip()

        if not value:

            raise serializers.ValidationError(
                "Drop location is required."
            )

        return value

    # =====================================================
    # LATITUDE VALIDATION
    # =====================================================

    def validate_pickup_latitude(self, value):

        if not -90 <= float(value) <= 90:

            raise serializers.ValidationError(
                "Pickup latitude must be between -90 and 90."
            )

        return value

    def validate_dropoff_latitude(self, value):

        if not -90 <= float(value) <= 90:

            raise serializers.ValidationError(
                "Dropoff latitude must be between -90 and 90."
            )

        return value

    # =====================================================
    # LONGITUDE VALIDATION
    # =====================================================

    def validate_pickup_longitude(self, value):

        if not -180 <= float(value) <= 180:

            raise serializers.ValidationError(
                "Pickup longitude must be between -180 and 180."
            )

        return value

    def validate_dropoff_longitude(self, value):

        if not -180 <= float(value) <= 180:

            raise serializers.ValidationError(
                "Dropoff longitude must be between -180 and 180."
            )

        return value

    # =====================================================
    # RIDE VALIDATION
    # =====================================================

    def validate(self, attrs):

        request = self.context["request"]

        pickup_latitude = attrs.get(
            "pickup_latitude"
        )

        pickup_longitude = attrs.get(
            "pickup_longitude"
        )

        dropoff_latitude = attrs.get(
            "dropoff_latitude"
        )

        dropoff_longitude = attrs.get(
            "dropoff_longitude"
        )

        # -------------------------------------------------
        # SAME LOCATION
        # -------------------------------------------------

        if (
            pickup_latitude == dropoff_latitude
            and
            pickup_longitude == dropoff_longitude
        ):

            raise serializers.ValidationError({
                "location":
                    "Pickup and drop locations "
                    "cannot be the same."
            })

        # -------------------------------------------------
        # ACTIVE RIDE
        # -------------------------------------------------

        active_statuses = [
            RideStatus.Status.REQUESTED,
            RideStatus.Status.ACCEPTED,
            RideStatus.Status.DRIVER_ARRIVING,
            RideStatus.Status.STARTED,
        ]

        active_ride_exists = (
            Ride.objects
            .filter(
                rider=request.user,
                status__name__in=active_statuses
            )
            .exists()
        )

        if active_ride_exists:

            raise serializers.ValidationError({
                "ride":
                    "You already have an active ride."
            })

        return attrs

    # =====================================================
    # CREATE RIDE
    # =====================================================

    def create(self, validated_data):

        request = self.context["request"]

        # -------------------------------------------------
        # GET REQUESTED STATUS
        # -------------------------------------------------

        try:

            requested_status = RideStatus.objects.get(
                name=RideStatus.Status.REQUESTED
            )

        except RideStatus.DoesNotExist:

            raise serializers.ValidationError({
                "status":
                    "Requested ride status is not configured."
            })

        # -------------------------------------------------
        # CALCULATE FARE
        # -------------------------------------------------

        try:

            fare_details = FareService.calculate_fare(

                vehicle_type=validated_data[
                    "vehicle_type"
                ],

                pickup_latitude=validated_data[
                    "pickup_latitude"
                ],

                pickup_longitude=validated_data[
                    "pickup_longitude"
                ],

                dropoff_latitude=validated_data[
                    "dropoff_latitude"
                ],

                dropoff_longitude=validated_data[
                    "dropoff_longitude"
                ],

                duration_minutes=0,
            )

        except ValueError as exc:

            raise serializers.ValidationError({
                "fare": str(exc)
            })

        except KeyError as exc:

            raise serializers.ValidationError({
                "fare":
                    f"Fare configuration is incomplete: {exc}"
            })

        # -------------------------------------------------
        # FINAL FARE
        # -------------------------------------------------

        final_fare = fare_details["total"]

        # -------------------------------------------------
        # CREATE RIDE
        # -------------------------------------------------

        ride = Ride.objects.create(

            rider=request.user,

            driver=None,

            status=requested_status,

            fare=final_fare,

            **validated_data
        )

        return ride


# =========================================================
# RIDE LIST SERIALIZER
# =========================================================

class RideSerializer(
    serializers.ModelSerializer
):

    vehicle_type = serializers.CharField(
        source="vehicle_type.name",
        read_only=True
    )

    status = serializers.CharField(
        source="status.name",
        read_only=True
    )

    class Meta:

        model = Ride

        fields = [
            "id",

            "pickup_address",
            "pickup_latitude",
            "pickup_longitude",

            "dropoff_address",
            "dropoff_latitude",
            "dropoff_longitude",

            "vehicle_type",

            "fare",

            "status",

            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "vehicle_type",
            "fare",
            "status",
            "created_at",
            "updated_at",
        ]


# =========================================================
# RIDE DETAIL SERIALIZER
# =========================================================

class RideDetailSerializer(
    serializers.ModelSerializer
):

    passenger = serializers.SerializerMethodField()

    driver = DriverNestedSerializer(
        read_only=True
    )

    vehicle = serializers.SerializerMethodField()

    status = serializers.CharField(
        source="status.name",
        read_only=True
    )

    vehicle_type = serializers.CharField(
        source="vehicle_type.name",
        read_only=True
    )

    class Meta:

        model = Ride

        fields = [
            "id",

            "passenger",

            "driver",

            "vehicle",

            "pickup_address",
            "pickup_latitude",
            "pickup_longitude",

            "dropoff_address",
            "dropoff_latitude",
            "dropoff_longitude",

            "vehicle_type",

            "status",

            "fare",

            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "passenger",
            "driver",
            "vehicle",
            "vehicle_type",
            "status",
            "fare",
            "created_at",
            "updated_at",
        ]

    # =====================================================
    # PASSENGER
    # =====================================================

    def get_passenger(self, obj):

        try:

            profile = obj.rider.profile

            return {
                "id": str(obj.rider.id),
                "email": obj.rider.email,
                "first_name": profile.first_name,
                "last_name": profile.last_name,
                "phone": profile.phone,
            }

        except Profile.DoesNotExist:

            return {
                "id": str(obj.rider.id),
                "email": obj.rider.email,
                "first_name": "",
                "last_name": "",
                "phone": "",
            }

    # =====================================================
    # VEHICLE
    # =====================================================

    def get_vehicle(self, obj):

        if not obj.driver:

            return None

        vehicle = (
            Vehicle.objects
            .select_related("vehicle_type")
            .filter(
                driver=obj.driver
            )
            .first()
        )

        if not vehicle:

            return None

        return {
            "id": str(vehicle.id),
            "type": vehicle.vehicle_type.name,
            "registration_number":
                vehicle.registration_number,
            "model": vehicle.model,
        }


# =========================================================
# RIDE STATUS UPDATE SERIALIZER
# =========================================================

# =========================================================
# RIDE STATUS UPDATE SERIALIZER
# =========================================================

class RideStatusUpdateSerializer(serializers.Serializer):

    status = serializers.ChoiceField(
        choices=RideStatus.Status.choices
    )

    def validate(self, attrs):

        new_status = attrs["status"]

        ride = self.context["ride"]

        current_status = ride.status.name

        # -------------------------------------------------
        # ALLOWED TRANSITIONS
        # -------------------------------------------------

        allowed_transitions = {

            RideStatus.Status.REQUESTED: [
                RideStatus.Status.ACCEPTED,
                RideStatus.Status.CANCELLED,
            ],

            RideStatus.Status.ACCEPTED: [
                RideStatus.Status.DRIVER_ARRIVING,
                RideStatus.Status.STARTED,
                RideStatus.Status.COMPLETED,
                RideStatus.Status.CANCELLED,
            ],

            RideStatus.Status.DRIVER_ARRIVING: [
                RideStatus.Status.STARTED,
                RideStatus.Status.CANCELLED,
            ],

            RideStatus.Status.STARTED: [
                RideStatus.Status.COMPLETED,
            ],

            RideStatus.Status.COMPLETED: [],

            RideStatus.Status.CANCELLED: [],
        }

        allowed_statuses = allowed_transitions.get(
            current_status,
            []
        )

        if new_status not in allowed_statuses:

            raise serializers.ValidationError({
                "status": (
                    f"Cannot change ride status "
                    f"from '{current_status}' "
                    f"to '{new_status}'."
                )
            })

        return attrs