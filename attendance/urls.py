from django.urls import path
from .views import (
    AttendanceListAPIView,
    AttendanceDetailAPIView,
    AttendanceCreateAPIView,
    AttendanceUpdateAPIView,
    AttendanceDeleteAPIView,
)

urlpatterns = [
    path("attendances/", AttendanceListAPIView.as_view(), name="attendance-list"),
    path("attendances/<int:pk>/", AttendanceDetailAPIView.as_view(), name="attendance-detail"),
    path("attendances/create/", AttendanceCreateAPIView.as_view(), name="attendance-create"),
    path("attendances/<int:pk>/update/", AttendanceUpdateAPIView.as_view(), name="attendance-update"),
    path("attendances/<int:pk>/delete/", AttendanceDeleteAPIView.as_view(), name="attendance-delete"),
]
