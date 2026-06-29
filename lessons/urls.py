from django.urls import path
from .views import (
    LessonListAPIView,
    LessonDetailAPIView,
    LessonCreateAPIView,
    LessonUpdateAPIView,
    LessonDeleteAPIView,
    LessonGenerateAPIView,
)

urlpatterns = [
    path("lessons/", LessonListAPIView.as_view(), name="lesson-list"),
    path("lessons/<int:pk>/", LessonDetailAPIView.as_view(), name="lesson-detail"),
    path("lessons/create/", LessonCreateAPIView.as_view(), name="lesson-create"),
    path("lessons/generate/", LessonGenerateAPIView.as_view(), name="lesson-generate"),
    path("lessons/<int:pk>/update/", LessonUpdateAPIView.as_view(), name="lesson-update"),
    path("lessons/<int:pk>/delete/", LessonDeleteAPIView.as_view(), name="lesson-delete"),
]
