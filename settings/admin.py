from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import (
    OrganizationSetting, Branch, Room, LessonTime,
    SMTPSetting, TelegramBotSetting, BackupSetting,
)


@admin.register(OrganizationSetting)
class OrganizationSettingAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_at")
    search_fields = ("name",)


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "phone", "created_at")
    search_fields = ("name",)


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "branch", "capacity")
    list_filter = ("branch",)
    search_fields = ("name",)


@admin.register(LessonTime)
class LessonTimeAdmin(admin.ModelAdmin):
    list_display = ("id", "label", "start_time", "end_time")
    search_fields = ("label",)


@admin.register(SMTPSetting)
class SMTPSettingAdmin(admin.ModelAdmin):
    list_display = ("id", "host", "port", "from_email")
    search_fields = ("host",)


@admin.register(TelegramBotSetting)
class TelegramBotSettingAdmin(admin.ModelAdmin):
    list_display = ("id", "is_active", "chat_id", "created_at")
    list_filter = ("is_active",)


@admin.register(BackupSetting)
class BackupSettingAdmin(admin.ModelAdmin):
    list_display = ("id", "schedule", "retention_days", "is_enabled", "last_backup_at")
    list_filter = ("schedule", "is_enabled")
