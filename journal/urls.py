from django.urls import path
from .views import (
    JournalDetailAPIView,
    JournalCommentListAPIView,
    JournalCommentCreateAPIView,
    JournalCommentUpdateAPIView,
    JournalCommentDeleteAPIView,
)

urlpatterns = [
    path("<int:pk>/", JournalDetailAPIView.as_view(), name="journal-detail"),
    path(
        "<int:lesson_pk>/comments/",
        JournalCommentListAPIView.as_view(),
        name="journal-comment-list",
    ),
    path(
        "<int:lesson_pk>/comments/create/",
        JournalCommentCreateAPIView.as_view(),
        name="journal-comment-create",
    ),
    path(
        "<int:lesson_pk>/comments/<int:pk>/update/",
        JournalCommentUpdateAPIView.as_view(),
        name="journal-comment-update",
    ),
    path(
        "<int:lesson_pk>/comments/<int:pk>/delete/",
        JournalCommentDeleteAPIView.as_view(),
        name="journal-comment-delete",
    ),
]
