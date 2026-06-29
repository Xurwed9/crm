from django.urls import path

from .views import (
    HomeworkListAPIView,
    HomeworkDetailAPIView,
    HomeworkCreateAPIView,
    HomeworkUpdateAPIView,
    HomeworkDeleteAPIView,
    SubmissionListAPIView,
    SubmissionDetailAPIView,
    SubmissionCreateAPIView,
    SubmissionGradeAPIView,
    SubmissionDeleteAPIView,
)

urlpatterns = [
    path("homeworks/", HomeworkListAPIView.as_view(), name="homework-list"),
    path("homeworks/<int:pk>/", HomeworkDetailAPIView.as_view(), name="homework-detail"),
    path("homeworks/create/", HomeworkCreateAPIView.as_view(), name="homework-create"),
    path("homeworks/<int:pk>/update/", HomeworkUpdateAPIView.as_view(), name="homework-update"),
    path("homeworks/<int:pk>/delete/", HomeworkDeleteAPIView.as_view(), name="homework-delete"),

    path("submissions/", SubmissionListAPIView.as_view(), name="submission-list"),
    path("submissions/<int:pk>/", SubmissionDetailAPIView.as_view(), name="submission-detail"),
    path("submissions/create/", SubmissionCreateAPIView.as_view(), name="submission-create"),
    path("submissions/<int:pk>/grade/", SubmissionGradeAPIView.as_view(), name="submission-grade"),
    path("submissions/<int:pk>/delete/", SubmissionDeleteAPIView.as_view(), name="submission-delete"),
]
