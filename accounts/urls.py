from django.urls import path
from . import views

urlpatterns = [
    path("users/", views.UserListAPIView.as_view(), name="user-list"),
    path("users/create/", views.UserCreateAPIView.as_view(), name="user-create"),
    path("users/<int:pk>/", views.UserDetailAPIView.as_view(), name="user-detail"),
    path("users/<int:pk>/update/", views.UserUpdateAPIView.as_view(), name="user-update"),
    path("users/<int:pk>/role/", views.ChangeRoleAPIView.as_view(), name="user-role"),
    path("users/<int:pk>/delete/", views.UserDeleteAPIView.as_view(), name="user-delete"),

    path("profile/", views.ProfileAPIView.as_view(), name="profile"),
    path("profile/image/", views.ProfileImageUpdateAPIView.as_view(), name="profile-image"),

    path("auth/login/", views.LoginAPIView.as_view(), name="login"),
    path("auth/logout/", views.LogoutAPIView.as_view(), name="logout"),
    path(
        "auth/change-password/",
        views.ChangePasswordAPIView.as_view(),
        name="change-password",
    ),
]