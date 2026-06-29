from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    UpdateAPIView,
    DestroyAPIView,
)

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Group
from .serializers import (
    GroupListSerializer,
    GroupDetailSerializer,
    GroupCreateUpdateSerializer,
)
from .permissions import IsAdmin


class GroupQuerysetMixin:

    def get_queryset(self):
        queryset = Group.objects.select_related(
            "course",
            "teacher",
        ).prefetch_related("students")

        user = self.request.user

        if user.role == "admin":
            return queryset

        if user.role == "teacher":
            return queryset.filter(teacher=user)

        if user.role == "student":
            return queryset.filter(students=user)

        return Group.objects.none()


class GroupListAPIView(GroupQuerysetMixin, ListAPIView):
    serializer_class = GroupListSerializer
    permission_classes = [IsAuthenticated]


class GroupDetailAPIView(GroupQuerysetMixin, RetrieveAPIView):
    serializer_class = GroupDetailSerializer
    permission_classes = [IsAuthenticated]


class GroupCreateAPIView(CreateAPIView):
    serializer_class = GroupCreateUpdateSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    queryset = Group.objects.all()


class GroupUpdateAPIView(UpdateAPIView):
    serializer_class = GroupCreateUpdateSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    queryset = Group.objects.all()
    http_method_names = ["patch"]


class GroupDeleteAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    queryset = Group.objects.all()

    def destroy(self, request, *args, **kwargs):
        group = self.get_object()
        group.delete()

        return Response(
            {"detail": "Group deleted successfully."},
            status=status.HTTP_200_OK,
        )