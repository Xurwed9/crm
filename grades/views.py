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

from .models import Grade
from .serializers import (
    GradeListSerializer,
    GradeDetailSerializer,
    GradeCreateUpdateSerializer,
)
from .permissions import (
    CanViewGrade,
    CanCreateGrade,
    CanEditGrade,
    CanDeleteGrade,
)


class GradeListAPIView(ListAPIView):

    serializer_class = GradeListSerializer
    permission_classes = [IsAuthenticated, CanViewGrade]
    filter_backends = [SearchFilter]
    search_fields = [
        "student__first_name",
        "student__last_name",
        "lesson__topic",
    ]

    def get_queryset(self):

        user = self.request.user

        queryset = Grade.objects.select_related(
            "lesson",
            "lesson__group",
            "lesson__course",
            "lesson__teacher",
            "student",
            "student__user",
        )

        if user.role == "admin":
            return queryset

        if user.role == "teacher":
            return queryset.filter(lesson__teacher=user)

        if user.role == "student":
            return queryset.filter(student__user=user)

        return Grade.objects.none()


class GradeDetailAPIView(RetrieveAPIView):

    serializer_class = GradeDetailSerializer
    permission_classes = [IsAuthenticated, CanViewGrade]

    def get_queryset(self):

        return Grade.objects.select_related(
            "lesson",
            "lesson__group",
            "lesson__course",
            "lesson__teacher",
            "student",
            "student__user",
        )


class GradeCreateAPIView(CreateAPIView):


    serializer_class = GradeCreateUpdateSerializer
    permission_classes = [IsAuthenticated, CanCreateGrade]

    def perform_create(self, serializer):

        user = self.request.user

        if user.role == "teacher":
            lesson = serializer.validated_data.get("lesson")

            if lesson.teacher != user:
                raise PermissionDenied(
                    _("You can only grade your own lessons.")
                )

            serializer.save(teacher=user)
        else:
            serializer.save()


class GradeUpdateAPIView(UpdateAPIView):

    serializer_class = GradeCreateUpdateSerializer
    permission_classes = [IsAuthenticated, CanEditGrade]
    http_method_names = ["patch"]

    def get_queryset(self):
        return Grade.objects.select_related(
            "lesson",
            "lesson__group",
            "lesson__course",
            "lesson__teacher",
            "student",
            "student__user",
        )


class GradeDeleteAPIView(DestroyAPIView):

    permission_classes = [IsAuthenticated, CanDeleteGrade]

    def get_queryset(self):
        return Grade.objects.select_related(
            "lesson",
            "lesson__group",
            "lesson__course",
            "lesson__teacher",
            "student",
            "student__user",
        )

    def destroy(self, request, *args, **kwargs):

        grade = self.get_object()
        grade.delete()

        return Response(
            {"detail": _("Grade deleted successfully.")},
            status=status.HTTP_200_OK,
        )
