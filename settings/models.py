from django.db import models
from django.utils.translation import gettext_lazy as _


class OrganizationSetting(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name=_("Name"),
    )
    logo = models.ImageField(
        upload_to="org/",
        blank=True,
        null=True,
        verbose_name=_("Logo"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created at"),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated at"),
    )

    class Meta:
        verbose_name = _("Organization setting")
        verbose_name_plural = _("Organization settings")

    def __str__(self):
        return self.name


class Branch(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name=_("Name"),
    )
    address = models.CharField(
        max_length=500,
        blank=True,
        verbose_name=_("Address"),
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name=_("Phone"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created at"),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated at"),
    )

    class Meta:
        verbose_name = _("Branch")
        verbose_name_plural = _("Branches")

    def __str__(self):
        return self.name


class Room(models.Model):
    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        related_name="rooms",
        verbose_name=_("Branch"),
    )
    name = models.CharField(
        max_length=255,
        verbose_name=_("Name"),
    )
    capacity = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Capacity"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created at"),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated at"),
    )

    class Meta:
        verbose_name = _("Room")
        verbose_name_plural = _("Rooms")

    def __str__(self):
        return f"{self.branch.name} - {self.name}"


class LessonTime(models.Model):
    label = models.CharField(
        max_length=100,
        help_text=_("e.g. 1-пара, 2-пара"),
        verbose_name=_("Label"),
    )
    start_time = models.TimeField(
        verbose_name=_("Start time"),
    )
    end_time = models.TimeField(
        verbose_name=_("End time"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created at"),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated at"),
    )

    class Meta:
        verbose_name = _("Lesson time")
        verbose_name_plural = _("Lesson times")
        ordering = ["start_time"]

    def __str__(self):
        return f"{self.label} ({self.start_time} - {self.end_time})"


class SMTPSetting(models.Model):
    host = models.CharField(
        max_length=255,
        verbose_name=_("Host"),
    )
    port = models.PositiveIntegerField(
        default=587,
        verbose_name=_("Port"),
    )
    use_tls = models.BooleanField(
        default=True,
        verbose_name=_("Use TLS"),
    )
    host_user = models.CharField(
        max_length=255,
        verbose_name=_("Host user"),
    )
    host_password = models.CharField(
        max_length=255,
        verbose_name=_("Host password"),
    )
    from_email = models.EmailField(
        verbose_name=_("From email"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created at"),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated at"),
    )

    class Meta:
        verbose_name = _("SMTP setting")
        verbose_name_plural = _("SMTP settings")

    def __str__(self):
        return self.host


class TelegramBotSetting(models.Model):
    bot_token = models.CharField(
        max_length=255,
        verbose_name=_("Bot token"),
    )
    chat_id = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("Chat ID"),
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Is active"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created at"),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated at"),
    )

    class Meta:
        verbose_name = _("Telegram bot setting")
        verbose_name_plural = _("Telegram bot settings")

    def __str__(self):
        return f"Bot {self.pk}"


class BackupSetting(models.Model):
    SCHEDULE_CHOICES = (
        ("daily", _("Daily")),
        ("weekly", _("Weekly")),
        ("monthly", _("Monthly")),
    )
    schedule = models.CharField(
        max_length=10,
        choices=SCHEDULE_CHOICES,
        default="daily",
        verbose_name=_("Schedule"),
    )
    retention_days = models.PositiveIntegerField(
        default=30,
        verbose_name=_("Retention days"),
    )
    is_enabled = models.BooleanField(
        default=True,
        verbose_name=_("Is enabled"),
    )
    last_backup_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Last backup at"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created at"),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated at"),
    )

    class Meta:
        verbose_name = _("Backup setting")
        verbose_name_plural = _("Backup settings")

    def __str__(self):
        return f"Backup - {self.get_schedule_display()}"
