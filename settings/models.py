from django.db import models


class OrganizationSetting(models.Model):
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to="org/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "organization setting"
        verbose_name_plural = "organization settings"

    def __str__(self):
        return self.name


class Branch(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=500, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "branch"
        verbose_name_plural = "branches"

    def __str__(self):
        return self.name


class Room(models.Model):
    branch = models.ForeignKey(
        Branch, on_delete=models.CASCADE, related_name="rooms"
    )
    name = models.CharField(max_length=255)
    capacity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "room"
        verbose_name_plural = "rooms"

    def __str__(self):
        return f"{self.branch.name} - {self.name}"


class LessonTime(models.Model):
    label = models.CharField(max_length=100, help_text="e.g. 1-пара, 2-пара")
    start_time = models.TimeField()
    end_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "lesson time"
        verbose_name_plural = "lesson times"
        ordering = ["start_time"]

    def __str__(self):
        return f"{self.label} ({self.start_time} - {self.end_time})"


class SMTPSetting(models.Model):
    host = models.CharField(max_length=255)
    port = models.PositiveIntegerField(default=587)
    use_tls = models.BooleanField(default=True)
    host_user = models.CharField(max_length=255)
    host_password = models.CharField(max_length=255)
    from_email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "SMTP setting"
        verbose_name_plural = "SMTP settings"

    def __str__(self):
        return self.host


class TelegramBotSetting(models.Model):
    bot_token = models.CharField(max_length=255)
    chat_id = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "telegram bot setting"
        verbose_name_plural = "telegram bot settings"

    def __str__(self):
        return f"Bot {self.pk}"


class BackupSetting(models.Model):
    SCHEDULE_CHOICES = (
        ("daily", "Daily"),
        ("weekly", "Weekly"),
        ("monthly", "Monthly"),
    )
    schedule = models.CharField(max_length=10, choices=SCHEDULE_CHOICES, default="daily")
    retention_days = models.PositiveIntegerField(default=30)
    is_enabled = models.BooleanField(default=True)
    last_backup_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "backup setting"
        verbose_name_plural = "backup settings"

    def __str__(self):
        return f"Backup - {self.get_schedule_display()}"
