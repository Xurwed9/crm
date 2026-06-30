from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.generics import (
    ListAPIView, RetrieveAPIView, DestroyAPIView, RetrieveUpdateAPIView,
)
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import User
from .models import NotificationLog, NotificationSetting
from .serializers import (
    NotificationLogListSerializer,
    NotificationLogDetailSerializer,
    SendNotificationSerializer,
    NotificationSettingSerializer,
)
from .services import send_notification


class IsAdmin(BasePermission):

    message = _("Only administrators can perform this action.")

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == "admin"
        )


class SendNotificationAPIView(APIView):

    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request):

        serializer = SendNotificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        recipient = User.objects.get(pk=serializer.validated_data["recipient_id"])
        channels = serializer.validated_data["channels"]
        event_type = serializer.validated_data["event_type"]
        extra_data = serializer.validated_data.get("extra_data", {})

        enabled_channels = []
        settings = getattr(recipient, "notification_settings", None)

        for ch in channels:
            if ch == "email" and recipient.email:
                if settings is None or settings.email_enabled:
                    enabled_channels.append(ch)
            elif ch == "sms" and recipient.phone_number:
                if settings is None or settings.sms_enabled:
                    enabled_channels.append(ch)
            elif ch == "telegram":
                chat_id = getattr(settings, "telegram_chat_id", None) if settings else None
                if chat_id:
                    if settings.telegram_enabled:
                        enabled_channels.append(ch)

        if not enabled_channels:
            return Response(
                {"detail": _("No enabled channels available for this recipient.")},
                status=status.HTTP_400_BAD_REQUEST,
            )

        results = send_notification(recipient, event_type, enabled_channels, extra_data)

        return Response(
            {"results": results},
            status=status.HTTP_200_OK,
        )


class NotificationLogListAPIView(ListAPIView):

    serializer_class = NotificationLogListSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_queryset(self):
        return NotificationLog.objects.select_related("recipient").all()


class NotificationLogDetailAPIView(RetrieveAPIView):

    serializer_class = NotificationLogDetailSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_queryset(self):
        return NotificationLog.objects.select_related("recipient").all()


class NotificationLogDeleteAPIView(DestroyAPIView):

    permission_classes = [IsAuthenticated, IsAdmin]

    def get_queryset(self):
        return NotificationLog.objects.all()

    def destroy(self, request, *args, **kwargs):
        log = self.get_object()
        log.delete()
        return Response(
            {"detail": _("Notification log deleted successfully.")},
            status=status.HTTP_200_OK,
        )


class NotificationSettingRetrieveUpdateAPIView(RetrieveUpdateAPIView):

    serializer_class = NotificationSettingSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "patch"]

    def get_object(self):

        user = self.request.user
        if user.role == "admin":
            user_id = self.request.query_params.get("user_id")
            if user_id:
                user = User.objects.get(pk=user_id)

        setting, _ = NotificationSetting.objects.get_or_create(user=user)
        return setting
