from django.urls import path

from .views import (
    GroupListAPIView,
    GroupDetailAPIView,
    GroupCreateAPIView,
    GroupUpdateAPIView,
    GroupDeleteAPIView,
)


urlpatterns = [
    path(
        "",
        GroupListAPIView.as_view(),
        name="group-list"
    ),
    path(
        "<int:pk>/",
        GroupDetailAPIView.as_view(),
        name="group-detail"
    ),
    path(
        "create/",
        GroupCreateAPIView.as_view(),
        name="group-create"
    ),
    path(
        "<int:pk>/update/",
        GroupUpdateAPIView.as_view(),
        name="group-update"
    ),
    path(
        "<int:pk>/delete/",
        GroupDeleteAPIView.as_view(),
        name="group-delete"
    ),
]