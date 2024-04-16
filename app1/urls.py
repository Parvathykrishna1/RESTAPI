from django.urls import path
from .views import UserListView, RoleCreateView, UserRegistrationView, RoleListView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('roles/', RoleCreateView.as_view(), name='role-create'),
    path('roleslist/', RoleListView.as_view(), name='role-list'),
]
