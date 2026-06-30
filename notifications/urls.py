from django.urls import path
from .views import (
    SendNotificationAPIView,
    NotificationLogListAPIView,
    NotificationLogDetailAPIView,
    NotificationLogDeleteAPIView,
    NotificationSettingRetrieveUpdateAPIView,
)

urlpatterns = [
    path("send/", SendNotificationAPIView.as_view(), name="notification-send"),
    path("logs/", NotificationLogListAPIView.as_view(), name="notification-log-list"),
    path("logs/<int:pk>/", NotificationLogDetailAPIView.as_view(), name="notification-log-detail"),
    path("logs/<int:pk>/delete/", NotificationLogDeleteAPIView.as_view(), name="notification-log-delete"),
    path("settings/", NotificationSettingRetrieveUpdateAPIView.as_view(), name="notification-settings"),
]
