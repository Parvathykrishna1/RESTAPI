from django.urls import path
from .views import *
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('userregister/',UserRegister.as_view(),name='userregister'),
    path('userlist/',UserList.as_view(),name='userlist'),
    path('refreshtoken/',jwt_views.TokenRefreshView.as_view(),name ='refreshtoken'),
    path('access_token/',jwt_views.TokenObtainPairView.as_view(),name ='access token'),
]
