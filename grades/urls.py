from django.urls import path
from .views import (
    GradeListAPIView,
    GradeDetailAPIView,
    GradeCreateAPIView,
    GradeUpdateAPIView,
    GradeDeleteAPIView,
)

urlpatterns = [
    path("grades/", GradeListAPIView.as_view(), name="grade-list"),
    path("grades/<int:pk>/", GradeDetailAPIView.as_view(), name="grade-detail"),
    path("grades/create/", GradeCreateAPIView.as_view(), name="grade-create"),
    path("grades/<int:pk>/update/", GradeUpdateAPIView.as_view(), name="grade-update"),
    path("grades/<int:pk>/delete/", GradeDeleteAPIView.as_view(), name="grade-delete"),
]
