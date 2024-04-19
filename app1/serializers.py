from rest_framework import serializers
from .models import *
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={"inut_type": "password"})
    first_name = serializers.CharField(required=True, allow_null=False)
    last_name = serializers.CharField(required=True, allow_null=False)

    class Meta:
        model = User
        fields = [
            "username",
            "password",
            "email",
            "first_name",
            "last_name",
            "mobile_phone",
            "status",
            "role_id",
        ]

    def save(self):
        reg = User(
            email=self.validated_data["email"],
            username=self.validated_data["username"],
            password=make_password(self.validated_data["password"]),
            mobile_phone=self.validated_data["mobile_phone"],
            role_id=self.validated_data["role_id"],
            first_name=self.validated_data["first_name"],
            last_name=self.validated_data["last_name"],
        )
        reg.save()


class UserSerializer(serializers.ModelSerializer):

    role = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()

    def get_role(self, instance):
        if instance.role_id:
            data = {"id": instance.role_id.role_id, "name": instance.role_id.name}
            return data

    def get_full_name(self, instance):
        if instance.first_name and instance.last_name:
            data = f"{instance.first_name} {instance.last_name}"
            return data

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "mobile_phone",
            "date_joined",
            "status",
            "role",
            "full_name",
            "user_id",
        ]


class LoginSerializer(serializers.Serializer):

    username = serializers.CharField(max_length=255)
    password = serializers.CharField(style={"input_type": "password"})


class LoginResponseSerializer(serializers.ModelSerializer):

    role = serializers.SerializerMethodField()
    access_token = serializers.SerializerMethodField()
    refresh_token = serializers.SerializerMethodField()

    def get_role(self, instance):
        data = {"id": instance.role_id.role_id, "name": instance.role_id.name}
        return data

    def get_refresh_token(self, instance):
        return str(RefreshToken.for_user(instance))

    def get_access_token(self, instance):
        return str(RefreshToken.for_user(instance).access_token)

    class Meta:
        model = User
        fields = [
            "user_id",
            "username",
            "email",
            "first_name",
            "last_name",
            "mobile_phone",
            "date_joined",
            "status",
            "role",
            "access_token",
            "refresh_token",
        ]

