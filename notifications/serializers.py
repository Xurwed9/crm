from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from .models import NotificationLog, NotificationSetting


class NotificationLogListSerializer(serializers.ModelSerializer):

    recipient = serializers.StringRelatedField()
    event_type_display = serializers.CharField(
        source="get_event_type_display",
        read_only=True,
    )
    channel_display = serializers.CharField(
        source="get_channel_display",
        read_only=True,
    )
    status_display = serializers.CharField(
        source="get_status_display",
        read_only=True,
    )

    class Meta:
        model = NotificationLog
        fields = (
            "id",
            "event_type",
            "event_type_display",
            "channel",
            "channel_display",
            "recipient",
            "subject",
            "status",
            "status_display",
            "sent_at",
            "created_at",
        )


class NotificationLogDetailSerializer(serializers.ModelSerializer):

    recipient = serializers.StringRelatedField()
    event_type_display = serializers.CharField(
        source="get_event_type_display",
        read_only=True,
    )
    channel_display = serializers.CharField(
        source="get_channel_display",
        read_only=True,
    )
    status_display = serializers.CharField(
        source="get_status_display",
        read_only=True,
    )

    class Meta:
        model = NotificationLog
        fields = (
            "id",
            "event_type",
            "event_type_display",
            "channel",
            "channel_display",
            "recipient",
            "subject",
            "body",
            "status",
            "status_display",
            "sent_at",
            "error_message",
            "created_at",
        )


class SendNotificationSerializer(serializers.Serializer):

    event_type = serializers.ChoiceField(
        choices=[
            "user_created", "homework_assigned", "exam_scheduled",
            "payment_reminder", "absent", "custom",
        ],
        label=_("Event type"),
    )
    recipient_id = serializers.IntegerField(
        label=_("Recipient ID"),
    )
    channels = serializers.ListField(
        child=serializers.ChoiceField(choices=["email", "sms", "telegram"]),
        label=_("Channels"),
    )
    extra_data = serializers.JSONField(required=False, default=dict, label=_("Extra data"))

    def validate_recipient_id(self, value):
        from accounts.models import User
        if not User.objects.filter(pk=value).exists():
            raise serializers.ValidationError(_("User does not exist."))
        return value


class NotificationSettingSerializer(serializers.ModelSerializer):

    class Meta:
        model = NotificationSetting
        fields = (
            "email_enabled",
            "sms_enabled",
            "telegram_enabled",
            "telegram_chat_id",
        )
