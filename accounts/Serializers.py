from django.contrib.auth.models import User
from rest_framework import serializers

from .models import UserProfile


class RegisterSerializer(serializers.Serializer):

    # User fields
    username = serializers.CharField(
        max_length=150
    )

    email = serializers.EmailField()

    password = serializers.CharField(
        write_only=True,
        min_length=6
    )

    # UserProfile fields
    phone = serializers.CharField(
        max_length=15,
        required=False,
        allow_blank=True
    )

    address = serializers.CharField(
        required=False,
        allow_blank=True
    )

    city = serializers.CharField(
        max_length=100,
        required=False,
        allow_blank=True
    )

    state = serializers.CharField(
        max_length=100,
        required=False,
        allow_blank=True
    )

    # pincode = serializers.CharField(
    #     max_length=10,
    #     required=False,
    #     allow_blank=True
    # )

    def validate_username(self, value):

        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                "Username already exists"
            )

        return value

    def validate_email(self, value):

        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "Email already exists"
            )

        return value

    def create(self, validated_data):

        # Create User
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"]
        )

        # Create UserProfile
        UserProfile.objects.create(
            user=user,
            phone=validated_data.get("phone",""),
            address=validated_data.get("address",""),
            city=validated_data.get("city",""),
            state=validated_data.get("state",""),
            # pincode=validated_data.get("pincode","")
        )

        return user