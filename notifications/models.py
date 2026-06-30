from django.db import models
from accounts.models import User


class NotificationSetting(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="notification_settings",
    )

    email_enabled = models.BooleanField(default=True)

    sms_enabled = models.BooleanField(default=False)

    telegram_enabled = models.BooleanField(default=False)

    telegram_chat_id = models.CharField(
        max_length=100,
        blank=True,
    )

    class Meta:
        verbose_name = "notification setting"
        verbose_name_plural = "notification settings"

    def __str__(self):
        return f"{self.user} settings"


class NotificationLog(models.Model):

    EVENT_CHOICES = (
        ("user_created", "User Created"),
        ("homework_assigned", "Homework Assigned"),
        ("exam_scheduled", "Exam Scheduled"),
        ("payment_reminder", "Payment Reminder"),
        ("absent", "Absent Notification"),
        ("custom", "Custom"),
    )

    CHANNEL_CHOICES = (
        ("email", "Email"),
        ("sms", "SMS"),
        ("telegram", "Telegram"),
    )

    STATUS_CHOICES = (
        ("sent", "Sent"),
        ("failed", "Failed"),
        ("pending", "Pending"),
    )

    event_type = models.CharField(
        max_length=20,
        choices=EVENT_CHOICES,
    )

    channel = models.CharField(
        max_length=10,
        choices=CHANNEL_CHOICES,
    )

    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="notifications",
    )

    subject = models.CharField(
        max_length=200,
    )

    body = models.TextField()

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="pending",
    )

    sent_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    error_message = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.get_event_type_display()} - {self.recipient} - {self.get_status_display()}"
