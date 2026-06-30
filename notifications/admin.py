from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import NotificationLog, NotificationSetting


@admin.register(NotificationSetting)
class NotificationSettingAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "email_enabled",
        "sms_enabled",
        "telegram_enabled",
        "telegram_chat_id",
    )

    search_fields = (
        "user__username",
        "user__first_name",
        "user__last_name",
    )

    def has_add_permission(self, request):
        return request.user.is_superuser or request.user.role == "admin"

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.role == "admin"

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.role == "admin"

    def has_view_permission(self, request, obj=None):
        return request.user.is_authenticated


@admin.register(NotificationLog)
class NotificationLogAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "event_type",
        "channel",
        "recipient",
        "subject",
        "status",
        "sent_at",
        "created_at",
    )

    list_filter = (
        "event_type",
        "channel",
        "status",
    )

    search_fields = (
        "subject",
        "recipient__username",
        "recipient__first_name",
        "recipient__last_name",
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.role == "admin"

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.role == "admin"
