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

from .models import Attendance
from .serializers import (
    AttendanceListSerializer,
    AttendanceDetailSerializer,
    AttendanceCreateUpdateSerializer,
)
from .permissions import (
    CanViewAttendance,
    CanCreateAttendance,
    CanEditAttendance,
    CanDeleteAttendance,
)


class AttendanceListAPIView(ListAPIView):

    serializer_class = AttendanceListSerializer
    permission_classes = [IsAuthenticated, CanViewAttendance]
    filter_backends = [SearchFilter]
    search_fields = [
        "student__first_name",
        "student__last_name",
        "lesson__topic",
    ]

    def get_queryset(self):

        user = self.request.user

        queryset = Attendance.objects.select_related(
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

        return Attendance.objects.none()


class AttendanceDetailAPIView(RetrieveAPIView):


    serializer_class = AttendanceDetailSerializer
    permission_classes = [IsAuthenticated, CanViewAttendance]

    def get_queryset(self):

        return Attendance.objects.select_related(
            "lesson",
            "lesson__group",
            "lesson__course",
            "lesson__teacher",
            "student",
            "student__user",
        )


class AttendanceCreateAPIView(CreateAPIView):

    serializer_class = AttendanceCreateUpdateSerializer
    permission_classes = [IsAuthenticated, CanCreateAttendance]

    def perform_create(self, serializer):

        user = self.request.user

        if user.role == "teacher":
            lesson = serializer.validated_data.get("lesson")

            if lesson.teacher != user:
                raise PermissionDenied(
                    _("You can only mark attendance for your own lessons.")
                )

        serializer.save()


class AttendanceUpdateAPIView(UpdateAPIView):

    serializer_class = AttendanceCreateUpdateSerializer
    permission_classes = [IsAuthenticated, CanEditAttendance]
    http_method_names = ["patch"]

    def get_queryset(self):
        return Attendance.objects.select_related(
            "lesson",
            "lesson__group",
            "lesson__course",
            "lesson__teacher",
            "student",
            "student__user",
        )


class AttendanceDeleteAPIView(DestroyAPIView):

    permission_classes = [IsAuthenticated, CanDeleteAttendance]

    def get_queryset(self):
        return Attendance.objects.select_related(
            "lesson",
            "lesson__group",
            "lesson__course",
            "lesson__teacher",
            "student",
            "student__user",
        )

    def destroy(self, request, *args, **kwargs):

        attendance = self.get_object()
        attendance.delete()

        return Response(
            {"detail": _("Attendance record deleted successfully.")},
            status=status.HTTP_200_OK,
        )
