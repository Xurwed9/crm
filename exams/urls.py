from django.urls import path
from .views import (
    ExamListAPIView,
    ExamDetailAPIView,
    ExamCreateAPIView,
    ExamUpdateAPIView,
    ExamDeleteAPIView,
    ExamResultListAPIView,
    ExamResultDetailAPIView,
    ExamResultCreateAPIView,
    ExamResultUpdateAPIView,
    ExamResultDeleteAPIView,
)

urlpatterns = [
    path("exams/", ExamListAPIView.as_view(), name="exam-list"),
    path("exams/<int:pk>/", ExamDetailAPIView.as_view(), name="exam-detail"),
    path("exams/create/", ExamCreateAPIView.as_view(), name="exam-create"),
    path("exams/<int:pk>/update/", ExamUpdateAPIView.as_view(), name="exam-update"),
    path("exams/<int:pk>/delete/", ExamDeleteAPIView.as_view(), name="exam-delete"),
    path("results/", ExamResultListAPIView.as_view(), name="examresult-list"),
    path("results/<int:pk>/", ExamResultDetailAPIView.as_view(), name="examresult-detail"),
    path("results/create/", ExamResultCreateAPIView.as_view(), name="examresult-create"),
    path("results/<int:pk>/update/", ExamResultUpdateAPIView.as_view(), name="examresult-update"),
    path("results/<int:pk>/delete/", ExamResultDeleteAPIView.as_view(), name="examresult-delete"),
]
