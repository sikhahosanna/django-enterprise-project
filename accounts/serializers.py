from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate

from .models import User


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        validators=[validate_password]
    )

    class Meta:
        model = User
        fields = ["email", "password"]


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


        if not user.check_password(data["current_password"]):

            raise serializers.ValidationError(
                "Current password is incorrect"
            )


        return data