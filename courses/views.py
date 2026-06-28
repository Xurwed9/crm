from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    UpdateAPIView,
    DestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated

from .models import Course
from .serializers import CourseSerializer
from .permissions import IsAdmin


class CourseListAPIView(ListAPIView):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Course.objects.all()


class CourseDetailAPIView(RetrieveAPIView):

    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Course.objects.all()


class CourseCreateAPIView(CreateAPIView):

    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsAdmin]


class CourseUpdateAPIView(UpdateAPIView):

    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    http_method_names = ["patch"]

    def get_queryset(self):
        return Course.objects.all()


class CourseDeleteAPIView(DestroyAPIView):

    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_queryset(self):
        return Course.objects.all()