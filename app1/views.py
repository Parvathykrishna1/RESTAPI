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
from rest_framework.views import APIView



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

#CreateAPIView
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

#APIView
# class UserRegister(APIView):

#     def post(self, request, *args, **kwargs):
#         serializer = UserRegistrationSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



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


# class UserList(APIView):
#     search_fields = ["username", "first_name", "last_name", "role_id__name"]
#     filter_backends = (filters.SearchFilter,)

#     def get_serializer_class(self):
#         return UserSerializer

#     def get_queryset(self):
#         queryset = User.objects.only(
#             "username",
#             "email",
#             "first_name",
#             "last_name",
#             "mobile_phone",
#             "date_joined",
#             "status",
#             "role_id__role_id",
#             "role_id__name",
#             "user_id",
#         ).select_related("role_id")
#         queryset = queryset.filter(status=0)
#         return queryset.order_by("-user_id")

#     def get(self, request, *args, **kwargs):
#         queryset = self.get_queryset()
#         queryset = self.filter_queryset(queryset)
#         serializer = self.get_serializer(queryset, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

class UserById(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.filter(status=0)
    serializer_class = UserSerializer

    def get(self, request, pk, format=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        instance = self.get_object()
        serializer = UserCreateUpdateSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "Status": "0",
                    "Message": "Successfully Updated!",
                    "Body": serializer.data,
                }
            )
        return Response(serializer.errors)

    def delete(self, request, pk, format=None):
        details = self.get_object()
        try:
            details.delete()
            return Response({"Status": "0", "Message": "User deleted"})
        except:
            return Response({"Status": "1", "Message": "Deletion failed!"})


# class UserById(APIView):
#     def get(self, request, pk, format=None):
#         try:
#             instance = User.objects.get(pk=pk, status=0)
#             serializer = UserSerializer(instance)
#             return Response(serializer.data)
#         except User.DoesNotExist:
#             return Response(
#                 {"message": "User not found", "status": "1"},
#                 status=status.HTTP_404_NOT_FOUND,
#             )

#     def put(self, request, pk, format=None):
#         try:
#             instance = User.objects.get(pk=pk, status=0)
#             serializer = UserCreateUpdateSerializer(instance, data=request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(
#                     {
#                         "Status": "0",
#                         "Message": "Successfully Updated!",
#                         "Body": serializer.data,
#                     }
#                 )
#             return Response(serializer.errors)
#         except User.DoesNotExist:
#             return Response(
#                 {"message": "User not found", "status": "1"},
#                 status=status.HTTP_404_NOT_FOUND,
#             )

#     def delete(self, request, pk, format=None):
#         try:
#             instance = User.objects.get(pk=pk, status=0)
#             instance.delete()
#             return Response({"Status": "0", "Message": "User deleted"})
#         except User.DoesNotExist:
#             return Response(
#                 {"message": "User not found", "status": "1"},
#                 status=status.HTTP_404_NOT_FOUND,
#             )

class Login(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer = LoginSerializer

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            try:
                try:
                    user_obj = User.objects.get(
                        Q(username__iexact=data["username"])
                        | Q(email__iexact=data["username"])
                    )
                    if user_obj:
                        if check_password(data["password"], user_obj.password):
                            user_obj.last_login = datetime.datetime.now()
                            user_obj.save()
                            refresh_token = RefreshToken.for_user(user_obj)

                            return Response(
                                {
                                    "message": "Successfully logged_in",
                                    "status": 0,
                                    "access_token": str(refresh_token.access_token),
                                    "refresh_token": str(refresh_token),
                                    "user_id": user_obj.user_id,
                                    "first_name": user_obj.first_name,
                                    "last_name": user_obj.last_name,
                                    "mobile_phone": user_obj.mobile_phone,
                                    "username": user_obj.username,
                                    "email": user_obj.email,
                                    "last_login": user_obj.last_login,
                                }
                            )
                            resp = LoginResponseSerializer(instance=user_obj)
                            return Response(resp.data, status=status.HTTP_200_OK)
                        else:
                            return Response(
                                {"message": "Invalid Password", "status": "1"}
                            )
                except Exception as e:
                    print(str(e))
                    return Response({"message": "Invalid User", "status": "1"})
                if user_obj.status != 0:
                    return Response({"message": "Inactive User", "status": "1"})
            except Exception as e:
                print("Login Error:", str(e))
        else:
            return Response(
                serializer.errors,
            )


# class Login(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         serializer = LoginSerializer(data=request.data)
#         if serializer.is_valid():
#             data = serializer.validated_data
#             try:
#                 user_obj = User.objects.get(
#                     Q(username__iexact=data["username"])
#                     | Q(email__iexact=data["username"]),
#                     status=0,
#                 )
#                 if check_password(data["password"], user_obj.password):
#                     user_obj.last_login = datetime.datetime.now()
#                     user_obj.save()
#                     refresh_token = RefreshToken.for_user(user_obj)

#                     return Response(
#                         {
#                             "message": "Successfully logged_in",
#                             "status": 0,
#                             "access_token": str(refresh_token.access_token),
#                             "refresh_token": str(refresh_token),
#                             "user_id": user_obj.user_id,
#                             "first_name": user_obj.first_name,
#                             "last_name": user_obj.last_name,
#                             "mobile_phone": user_obj.mobile_phone,
#                             "username": user_obj.username,
#                             "email": user_obj.email,
#                             "last_login": user_obj.last_login,
#                         }
#                     )
#                 else:
#                     return Response({"message": "Invalid Password", "status": "1"})
#             except User.DoesNotExist:
#                 return Response(
#                     {"message": "Invalid User", "status": "1"},
#                     status=status.HTTP_404_NOT_FOUND,
#                 )
#         else:
#             return Response(
#                 serializer.errors,
#                 status=status.HTTP_400_BAD_REQUEST,
#             )
