from rest_framework import status
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    UpdateAPIView,
    DestroyAPIView,
    GenericAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.filters import SearchFilter

from groups.models import Group

from .models import Lesson
from .serializers import (
    LessonListSerializer,
    LessonDetailSerializer,
    LessonCreateUpdateSerializer,
    LessonGenerateSerializer,
)
from .permissions import (
    CanViewLesson,
    CanCreateLesson,
    CanEditLesson,
    CanDeleteLesson,
)
from .utils import generate_lessons_for_group


class LessonListAPIView(ListAPIView):

    serializer_class = LessonListSerializer
    permission_classes = [IsAuthenticated, CanViewLesson]
    filter_backends = [SearchFilter]
    search_fields = [
        "topic",
        "group__name",
        "course__name",
        "lesson_date",
    ]

    def get_queryset(self):

        user = self.request.user

        queryset = Lesson.objects.select_related(
            "group",
            "course",
            "teacher",
        )

        if user.role == "admin":
            return queryset

        if user.role == "teacher":
            return queryset.filter(group__teacher=user)

        if user.role == "student":
            return queryset.filter(group__students__user=user)

        return Lesson.objects.none()


class LessonDetailAPIView(RetrieveAPIView):

    serializer_class = LessonDetailSerializer
    permission_classes = [IsAuthenticated, CanViewLesson]

    def get_queryset(self):

        return Lesson.objects.select_related(
            "group",
            "course",
            "teacher",
        )


class LessonCreateAPIView(CreateAPIView):

    serializer_class = LessonCreateUpdateSerializer
    permission_classes = [IsAuthenticated, CanCreateLesson]

    def perform_create(self, serializer):

        user = self.request.user

        if user.role == "teacher":
            serializer.save(teacher=user)
        else:
            serializer.save()


class LessonUpdateAPIView(UpdateAPIView):

    serializer_class = LessonCreateUpdateSerializer
    permission_classes = [IsAuthenticated, CanEditLesson]
    http_method_names = ["patch"]

    def get_queryset(self):
        return Lesson.objects.select_related(
            "group",
            "course",
            "teacher",
        )


class LessonDeleteAPIView(DestroyAPIView):

    permission_classes = [IsAuthenticated, CanDeleteLesson]

    def get_queryset(self):
        return Lesson.objects.select_related(
            "group",
            "course",
            "teacher",
        )

    def destroy(self, request, *args, **kwargs):

        lesson = self.get_object()
        lesson.delete()

        return Response(
            {"detail": "Lesson deleted successfully."},
            status=status.HTTP_200_OK,
        )


class LessonGenerateAPIView(GenericAPIView):

    serializer_class = LessonGenerateSerializer
    permission_classes = [IsAuthenticated, CanCreateLesson]

    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        group_id = serializer.validated_data["group_id"]

        try:
            group = Group.objects.get(id=group_id)
        except Group.DoesNotExist:
            return Response(
                {"detail": "Group not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if request.user.role == "teacher" and group.teacher != request.user:
            return Response(
                {
                    "detail": "You can only generate lessons for your own groups."
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        count = generate_lessons_for_group(group)

        return Response(
            {"detail": f"{count} lessons generated successfully."},
            status=status.HTTP_201_CREATED,
        )
