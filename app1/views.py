import datetime
from django.contrib.auth.hashers import check_password
from django.db.models import Q
from rest_framework import generics
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import filters, status
from .models import *
from .serializers import *


def passwordrule(password):
    alphabets = digits = special = 0
    password_rule = PasswordRule.objects.filter(status=0).first()
    for i in range(len(password)):
        if password[i].isalpha():
            alphabets = alphabets + 1
        elif password[i].isdigit():
            digits = digits + 1
        else:
            special = special + 1
    if password_rule.minimumcharaters > len(
        password
    ) or password_rule.maximumcharaters < len(password):
        return {
            "Status": "1",
            "Message": "Password length must be greater than eight characters or less than fifteen character",
        }
    if special > password_rule.specialcharaters or special == 0:
        return {
            "Status": "1",
            "Message": "The password must contain at least one special character and  at most three special characters",
        }
    if digits < password_rule.uppercase:
        return {
            "Status": "1",
            "Message": "The password must contain at least one digit",
        }


class UserRegister(generics.CreateAPIView):

    def get_serializer_class(self):
        return UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(serializer.errors)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save()


class UserList(generics.ListAPIView):
    search_fields = ["username", "first_name", "last_name", "role_id__name"]
    filter_backends = (filters.SearchFilter,)

    def get_serializer_class(self):
        return UserSerializer

    def get_queryset(self):
        queryset = User.objects.only(
            "username",
            "email",
            "first_name",
            "last_name",
            "mobile_phone",
            "date_joined",
            "status",
            "role_id__role_id",
            "role_id__name",
            "user_id",
        ).select_related("role_id")
        queryset = queryset.filter(status=0)

        return queryset.order_by("-user_id")

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
