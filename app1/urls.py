from django.urls import path
from .views import *
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('login/',Login.as_view(),name='login'),
    path('userregister/',UserRegister.as_view(),name='userregister'),
    path('userlist/',UserList.as_view(),name='userlist'),
<<<<<<< HEAD
    path('userbyid/<int:pk>/',UserById.as_view(),name='userbyid'),
    path('users/bulk_delete/', BulkDeleteUsers.as_view(), name='bulk_delete_users'),
=======
>>>>>>> c48ea745d333e6b7a9b120eaf5c03fdda11e669a
    path('refreshtoken/',jwt_views.TokenRefreshView.as_view(),name ='refreshtoken'),
    path('access_token/',jwt_views.TokenObtainPairView.as_view(),name ='access token'),
]
