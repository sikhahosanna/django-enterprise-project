
from rest_framework import serializers

from django.core.validators import FileExtensionValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from django.db import transaction

import re

from .models import (
    User,
    Profile,
    DriverProfile,
    Vehicle,
    VehicleType,
)


# =========================================
# REGISTER SERIALIZER
# =========================================

class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        validators=[validate_password]
    )

    class Meta:
        model = User

        fields = [
            "email",
            "password"
        ]

    def validate_email(self, value):

        if User.objects.filter(
            email=value
        ).exists():

            raise serializers.ValidationError(
                "Email already exists"
            )

        return value

    def create(self, validated_data):

        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"]
        )

        return user


# =========================================
# LOGIN SERIALIZER
# =========================================

class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField()

    password = serializers.CharField(
        write_only=True
    )

    def validate(self, data):

        user = authenticate(
            email=data["email"],
            password=data["password"]
        )

        if not user:

            raise serializers.ValidationError(
                "Invalid email or password"
            )

        data["user"] = user

        return data


# =========================================
# CHANGE PASSWORD SERIALIZER
# =========================================

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
                "Current password is incorrect"
            )

        return data


# =========================================
# PROFILE SERIALIZER
# =========================================

class ProfileSerializer(serializers.ModelSerializer):

    profile_image = serializers.ImageField(
        required=False,
        validators=[
            FileExtensionValidator(
                allowed_extensions=[
                    "jpg",
                    "jpeg",
                    "png"
                ]
            )
        ]
    )

    class Meta:
        model = Profile

        fields = "__all__"

        read_only_fields = [
            "user"
        ]

    def validate_phone(self, value):

        if not re.match(
            r"^[0-9]{10}$",
            value
        ):

            raise serializers.ValidationError(
                "Phone number must be 10 digits"
            )

        return value

    def validate_profile_image(self, image):

        if image.size > 5 * 1024 * 1024:

            raise serializers.ValidationError(
                "Image size should be less than 5MB"
            )

        return image


# =========================================
# DRIVER SERIALIZER
# CREATE / UPDATE
# =========================================

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
        ]

    def validate_email(self, value):

        if User.objects.filter(
            email=value
        ).exists():

            raise serializers.ValidationError(
                "Email already exists"
            )

        return value

    @transaction.atomic
    def create(self, validated_data):

        email = validated_data.pop("email")
        password = validated_data.pop("password")

        first_name = validated_data.pop("first_name")
        last_name = validated_data.pop("last_name")
        phone = validated_data.pop("phone")

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
            **validated_data
        )

        return driver


# =========================================
# VEHICLE SERIALIZER
# CREATE / UPDATE
# =========================================

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

        extra_kwargs = {
            "registration_number": {
                "required": True
            },
            "model": {
                "required": True
            },
        }

    # Registration number validation
    def validate_registration_number(self, value):

        value = value.strip().upper()

        if not re.match(
            r"^[A-Z]{2}[0-9]{2}[A-Z]{1,2}[0-9]{4}$",
            value
        ):

            raise serializers.ValidationError(
                "Invalid vehicle registration number."
            )

        queryset = Vehicle.objects.filter(
            registration_number=value
        )

        # Ignore current vehicle during PATCH/PUT
        if self.instance:

            queryset = queryset.exclude(
                pk=self.instance.pk
            )

        if queryset.exists():

            raise serializers.ValidationError(
                "Vehicle with this registration number already exists."
            )

        return value

    # Vehicle type validation
    def validate_vehicle_type(self, value):

        if not VehicleType.objects.filter(
            pk=value.pk
        ).exists():

            raise serializers.ValidationError(
                "Invalid vehicle type."
            )

        return value

    # Driver validation
    def validate_driver(self, value):

        if not DriverProfile.objects.filter(
            pk=value.pk
        ).exists():

            raise serializers.ValidationError(
                "Invalid driver ID."
            )

        return value

    # Object-level validation
    def validate(self, attrs):

        driver = attrs.get("driver")
        vehicle_type = attrs.get("vehicle_type")

        # For POST both are required.
        # For PATCH, missing fields can be allowed.
        if not self.instance:

            if driver is None:

                raise serializers.ValidationError({
                    "driver": "Driver is required."
                })

            if vehicle_type is None:

                raise serializers.ValidationError({
                    "vehicle_type": "Vehicle type is required."
                })

        return attrs


# =========================================
# VEHICLE NESTED SERIALIZER
# =========================================

class VehicleNestedSerializer(serializers.ModelSerializer):

    type = serializers.CharField(
        source="vehicle_type.name"
    )

    class Meta:
        model = Vehicle

        fields = [
            "type",
            "registration_number"
        ]


# =========================================
# DRIVER NESTED SERIALIZER
# TASK 5
# =========================================

class DriverNestedSerializer(serializers.ModelSerializer):

    name = serializers.SerializerMethodField()

    vehicle = serializers.SerializerMethodField()

    class Meta:
        model = DriverProfile

        fields = [
            "id",
            "name",
            "vehicle"
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
