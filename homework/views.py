from django.utils import timezone

from rest_framework import status
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    UpdateAPIView,
    DestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.filters import SearchFilter

from .models import Homework, Submission
from .serializers import (
    HomeworkListSerializer,
    HomeworkDetailSerializer,
    HomeworkCreateUpdateSerializer,
    SubmissionListSerializer,
    SubmissionDetailSerializer,
    SubmissionCreateSerializer,
    SubmissionGradeSerializer,
)
from .permissions import (
    CanViewHomework,
    CanCreateHomework,
    CanEditHomework,
    CanDeleteHomework,
    CanViewSubmission,
    CanCreateSubmission,
    CanGradeSubmission,
    CanDeleteSubmission,
)

class HomeworkListAPIView(ListAPIView):

    serializer_class = HomeworkListSerializer
    permission_classes = [IsAuthenticated, CanViewHomework]
    filter_backends = [SearchFilter]
    search_fields = [
        "title",
        "lesson__topic",
    ]

    def get_queryset(self):

        user = self.request.user

        queryset = Homework.objects.select_related(
            "lesson__group",
            "lesson__course",
            "lesson__teacher",
        )

        if user.role == "admin":
            return queryset

        if user.role == "teacher":
            return queryset.filter(lesson__teacher=user)

        if user.role == "student":
            return queryset.filter(lesson__group__students__user=user)

        return Homework.objects.none()


class HomeworkDetailAPIView(RetrieveAPIView):

    serializer_class = HomeworkDetailSerializer
    permission_classes = [IsAuthenticated, CanViewHomework]

    def get_queryset(self):

        return Homework.objects.select_related(
            "lesson__group",
            "lesson__course",
            "lesson__teacher",
        )


class HomeworkCreateAPIView(CreateAPIView):

    serializer_class = HomeworkCreateUpdateSerializer
    permission_classes = [IsAuthenticated, CanCreateHomework]

    def perform_create(self, serializer):
        serializer.save()


class HomeworkUpdateAPIView(UpdateAPIView):

    serializer_class = HomeworkCreateUpdateSerializer
    permission_classes = [IsAuthenticated, CanEditHomework]
    http_method_names = ["patch"]

    def get_queryset(self):
        return Homework.objects.select_related(
            "lesson__group",
            "lesson__course",
            "lesson__teacher",
        )


class HomeworkDeleteAPIView(DestroyAPIView):

    permission_classes = [IsAuthenticated, CanDeleteHomework]

    def get_queryset(self):
        return Homework.objects.select_related(
            "lesson__group",
            "lesson__course",
            "lesson__teacher",
        )

    def destroy(self, request, *args, **kwargs):

        homework = self.get_object()
        homework.delete()

        return Response(
            {"detail": "Homework deleted successfully."},
            status=status.HTTP_200_OK,
        )

class SubmissionListAPIView(ListAPIView):

    serializer_class = SubmissionListSerializer
    permission_classes = [IsAuthenticated, CanViewSubmission]
    filter_backends = [SearchFilter]
    search_fields = [
        "homework__title",
        "student__first_name",
        "student__last_name",
    ]

    def get_queryset(self):

        user = self.request.user

        queryset = Submission.objects.select_related(
            "homework",
            "student",
        )

        if user.role == "admin":
            return queryset

        if user.role == "teacher":
            return queryset.filter(homework__lesson__teacher=user)

        if user.role == "student":
            return queryset.filter(student__user=user)

        return Submission.objects.none()


class SubmissionDetailAPIView(RetrieveAPIView):

    serializer_class = SubmissionDetailSerializer
    permission_classes = [IsAuthenticated, CanViewSubmission]

    def get_queryset(self):

        return Submission.objects.select_related(
            "homework__lesson",
            "student__user",
        )


class SubmissionCreateAPIView(CreateAPIView):

    serializer_class = SubmissionCreateSerializer
    permission_classes = [IsAuthenticated, CanCreateSubmission]

    def perform_create(self, serializer):

        try:
            student = self.request.user.student
        except Exception:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied(
                "Student profile not found. Please contact admin."
            )
        serializer.save(student=student)


class SubmissionGradeAPIView(UpdateAPIView):

    serializer_class = SubmissionGradeSerializer
    permission_classes = [IsAuthenticated, CanGradeSubmission]
    http_method_names = ["patch"]

    def get_queryset(self):

        return Submission.objects.select_related(
            "homework__lesson",
            "student__user",
        )

    def perform_update(self, serializer):

        serializer.save(graded_at=timezone.now())


class SubmissionDeleteAPIView(DestroyAPIView):

    permission_classes = [IsAuthenticated, CanDeleteSubmission]

    def get_queryset(self):
        return Submission.objects.select_related(
            "homework__lesson",
            "student__user",
        )

    def destroy(self, request, *args, **kwargs):

        submission = self.get_object()
        submission.delete()

        return Response(
            {"detail": "Submission deleted successfully."},
            status=status.HTTP_200_OK,
        )
