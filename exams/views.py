from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
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

from .models import Exam, ExamResult
from .serializers import (
    ExamListSerializer,
    ExamDetailSerializer,
    ExamCreateUpdateSerializer,
    ExamResultListSerializer,
    ExamResultDetailSerializer,
    ExamResultCreateUpdateSerializer,
)
from .permissions import (
    CanViewExam,
    CanCreateExam,
    CanEditExam,
    CanDeleteExam,
    CanViewExamResult,
    CanCreateExamResult,
    CanEditExamResult,
    CanDeleteExamResult,
)


class ExamListAPIView(ListAPIView):

    serializer_class = ExamListSerializer
    permission_classes = [IsAuthenticated, CanViewExam]
    filter_backends = [SearchFilter]
    search_fields = [
        "title",
        "lesson__topic",
        "lesson__group__name",
    ]

    def get_queryset(self):

        user = self.request.user

        queryset = Exam.objects.select_related(
            "lesson",
            "lesson__group",
            "lesson__course",
            "lesson__teacher",
        )

        if user.role == "admin":
            return queryset

        if user.role == "teacher":
            return queryset.filter(lesson__group__teacher=user)

        if user.role == "student":
            return queryset.filter(lesson__group__students__user=user)

        return Exam.objects.none()


class ExamDetailAPIView(RetrieveAPIView):

    serializer_class = ExamDetailSerializer
    permission_classes = [IsAuthenticated, CanViewExam]

    def get_queryset(self):

        return Exam.objects.select_related(
            "lesson",
            "lesson__group",
            "lesson__course",
            "lesson__teacher",
        )


class ExamCreateAPIView(CreateAPIView):

    serializer_class = ExamCreateUpdateSerializer
    permission_classes = [IsAuthenticated, CanCreateExam]

    def perform_create(self, serializer):

        user = self.request.user

        if user.role == "teacher":
            lesson = serializer.validated_data.get("lesson")

            if lesson.group.teacher != user:
                raise PermissionDenied(
                    _("You can only create exams for your own lessons.")
                )

        serializer.save()


class ExamUpdateAPIView(UpdateAPIView):

    serializer_class = ExamCreateUpdateSerializer
    permission_classes = [IsAuthenticated, CanEditExam]
    http_method_names = ["patch"]

    def get_queryset(self):
        return Exam.objects.select_related(
            "lesson",
            "lesson__group",
            "lesson__course",
            "lesson__teacher",
        )


class ExamDeleteAPIView(DestroyAPIView):

    permission_classes = [IsAuthenticated, CanDeleteExam]

    def get_queryset(self):
        return Exam.objects.select_related(
            "lesson",
            "lesson__group",
            "lesson__course",
            "lesson__teacher",
        )

    def destroy(self, request, *args, **kwargs):

        exam = self.get_object()
        exam.delete()

        return Response(
            {"detail": _("Exam deleted successfully.")},
            status=status.HTTP_200_OK,
        )


class ExamResultListAPIView(ListAPIView):

    serializer_class = ExamResultListSerializer
    permission_classes = [IsAuthenticated, CanViewExamResult]
    filter_backends = [SearchFilter]
    search_fields = [
        "student__first_name",
        "student__last_name",
        "exam__title",
    ]

    def get_queryset(self):

        user = self.request.user

        queryset = ExamResult.objects.select_related(
            "exam",
            "exam__lesson",
            "exam__lesson__group",
            "student",
            "student__user",
        )

        if user.role == "admin":
            return queryset

        if user.role == "teacher":
            return queryset.filter(exam__lesson__group__teacher=user)

        if user.role == "student":
            return queryset.filter(student__user=user)

        return ExamResult.objects.none()


class ExamResultDetailAPIView(RetrieveAPIView):

    serializer_class = ExamResultDetailSerializer
    permission_classes = [IsAuthenticated, CanViewExamResult]

    def get_queryset(self):

        return ExamResult.objects.select_related(
            "exam",
            "exam__lesson",
            "exam__lesson__group",
            "student",
            "student__user",
        )


class ExamResultCreateAPIView(CreateAPIView):

    serializer_class = ExamResultCreateUpdateSerializer
    permission_classes = [IsAuthenticated, CanCreateExamResult]

    def perform_create(self, serializer):

        user = self.request.user

        if user.role == "teacher":
            exam = serializer.validated_data.get("exam")

            if exam.lesson.group.teacher != user:
                raise PermissionDenied(
                    _("You can only enter results for your own exams.")
                )

        serializer.save()


class ExamResultUpdateAPIView(UpdateAPIView):

    serializer_class = ExamResultCreateUpdateSerializer
    permission_classes = [IsAuthenticated, CanEditExamResult]
    http_method_names = ["patch"]

    def get_queryset(self):
        return ExamResult.objects.select_related(
            "exam",
            "exam__lesson",
            "exam__lesson__group",
            "student",
            "student__user",
        )


class ExamResultDeleteAPIView(DestroyAPIView):

    permission_classes = [IsAuthenticated, CanDeleteExamResult]

    def get_queryset(self):
        return ExamResult.objects.select_related(
            "exam",
            "exam__lesson",
            "exam__lesson__group",
            "student",
            "student__user",
        )

    def destroy(self, request, *args, **kwargs):

        result = self.get_object()
        result.delete()

        return Response(
            {"detail": _("Exam result deleted successfully.")},
            status=status.HTTP_200_OK,
        )
