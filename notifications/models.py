from django.db import models
from django.utils.translation import gettext_lazy as _

from accounts.models import User


class NotificationSetting(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="notification_settings",
        verbose_name=_("User"),
    )

    email_enabled = models.BooleanField(
        default=True,
        verbose_name=_("Email enabled"),
    )

    sms_enabled = models.BooleanField(
        default=False,
        verbose_name=_("SMS enabled"),
    )

    telegram_enabled = models.BooleanField(
        default=False,
        verbose_name=_("Telegram enabled"),
    )

    telegram_chat_id = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("Telegram chat ID"),
    )

    class Meta:
        verbose_name = _("Notification setting")
        verbose_name_plural = _("Notification settings")

    def __str__(self):
        return f"{self.user} settings"


class NotificationLog(models.Model):

    EVENT_CHOICES = (
        ("user_created", _("User Created")),
        ("homework_assigned", _("Homework Assigned")),
        ("exam_scheduled", _("Exam Scheduled")),
        ("payment_reminder", _("Payment Reminder")),
        ("absent", _("Absent Notification")),
        ("custom", _("Custom")),
    )

    CHANNEL_CHOICES = (
        ("email", _("Email")),
        ("sms", _("SMS")),
        ("telegram", _("Telegram")),
    )

    STATUS_CHOICES = (
        ("sent", _("Sent")),
        ("failed", _("Failed")),
        ("pending", _("Pending")),
    )

    event_type = models.CharField(
        max_length=20,
        choices=EVENT_CHOICES,
        verbose_name=_("Event type"),
    )

    channel = models.CharField(
        max_length=10,
        choices=CHANNEL_CHOICES,
        verbose_name=_("Channel"),
    )

    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="notifications",
        verbose_name=_("Recipient"),
    )

    subject = models.CharField(
        max_length=200,
        verbose_name=_("Subject"),
    )

    body = models.TextField(
        verbose_name=_("Body"),
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="pending",
        verbose_name=_("Status"),
    )

    sent_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Sent at"),
    )

    error_message = models.TextField(
        blank=True,
        verbose_name=_("Error message"),
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created at"),
    )

    class Meta:
        verbose_name = _("Notification log")
        verbose_name_plural = _("Notification logs")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.get_event_type_display()} - {self.recipient} - {self.get_status_display()}"
