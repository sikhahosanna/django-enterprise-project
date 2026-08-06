from rest_framework import serializers

from django.core.validators import FileExtensionValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate

import re

from .models import User, Profile



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



    # Duplicate email check
    def validate_email(self, value):

        if User.objects.filter(email=value).exists():

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



    # Phone validation
    def validate_phone(self, value):

        if not re.match(
            r'^[0-9]{10}$',
            value
        ):

            raise serializers.ValidationError(
                "Phone number must be 10 digits"
            )


        return value



    # Image size validation
    def validate_profile_image(self, image):

        if image.size > 5 * 1024 * 1024:

            raise serializers.ValidationError(
                "Image size should be less than 5MB"
            )


        return image