from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    GenericAPIView,
)
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.tokens import RefreshToken

from .permissions import IsAdmin
from .serializers import (
    AdminUserUpdateSerializer,
    ChangePasswordSerializer,
    ChangeRoleSerializer,
    LoginSerializer,
    LogoutSerializer,
    ProfileImageUpdateSerializer,
    ProfileSerializer,
    UserCreateSerializer,
    UserDetailSerializer,
    UserListSerializer,
)
from rest_framework.parsers import MultiPartParser, FormParser
User = get_user_model()


class UserListAPIView(ListAPIView):
    serializer_class = UserListSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    filter_backends = [SearchFilter]
    search_fields = ["username", "phone_number", "email","first_name","last_name"]

    def get_queryset(self):
        return (
            User.objects.select_related("profile").all())


class UserDetailAPIView(RetrieveAPIView):
    serializer_class = UserDetailSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_queryset(self):
        return User.objects.select_related("profile").all()


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserCreateSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(
            {
                "detail": "Корбар сохта шуд ва маълумоти вуруд ба email фиристода шуд.",
                "user": UserDetailSerializer(
                    user, context=self.get_serializer_context()
                ).data,
            },
            status=status.HTTP_201_CREATED,
        )


class UserUpdateAPIView(UpdateAPIView):
    serializer_class = AdminUserUpdateSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    http_method_names = ["patch"]

    def get_queryset(self):
        return User.objects.all().select_related('profile')

class UserDeleteAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    queryset = User.objects.all()

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()

        if user == request.user:
            return Response(
                {"detail": "Шумо наметавонед аккаунти худро нест кунед."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.delete()

        return Response(
            {"detail": "Корбар пурра нест карда шуд."},
            status=status.HTTP_204_NO_CONTENT,
        )


class ProfileAPIView(RetrieveAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        profile = getattr(self.request.user, "profile", None)
        if profile is None:
            from rest_framework.exceptions import NotFound
            raise NotFound("Профил ёфт нашуд.")
        return profile

class ProfileImageUpdateAPIView(UpdateAPIView):
    serializer_class = ProfileImageUpdateSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    http_method_names = ["patch"]

    def get_object(self):
        profile = getattr(self.request.user, "profile", None)
        if profile is None:
            from rest_framework.exceptions import NotFound
            raise NotFound("Профил ёфт нашуд.")
        return profile


class LoginAPIView(GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "full_name": user.get_full_name(),
                    "email": user.email,
                    "role": user.role,
                },
            },
            status=status.HTTP_200_OK,
        )


class LogoutAPIView(GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"detail": "Шумо бомуваффақият баромадед."},
            status=status.HTTP_200_OK,
        )


class ChangePasswordAPIView(GenericAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        new_password = serializer.validated_data["new_password"]

        user.set_password(new_password)
        user.save(update_fields=["password"])

        refresh_token = request.data.get("refresh")
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except (TokenError, InvalidToken):
                pass

        return Response(
            {"detail": "Парол бомуваффақият иваз шуд. Лутфан дубора ворид шавед."},
            status=status.HTTP_200_OK,
        )

class ChangeRoleAPIView(GenericAPIView):
    serializer_class = ChangeRoleSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_object(self):
        return get_object_or_404(User, pk=self.kwargs["pk"])

    def patch(self, request, *args, **kwargs):
        user = self.get_object()

        if user == request.user:
            return Response(
                {"detail": "Шумо наметавонед нақши худро иваз кунед."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                "detail": f"Нақши корбар ба «{user.get_role_display()}» иваз шуд.",
                "user_id": user.id,
                "new_role": user.role,
            },
            status=status.HTTP_200_OK,
        )
