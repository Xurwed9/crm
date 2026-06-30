from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import JournalComment


@admin.register(JournalComment)
class JournalCommentAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "lesson",
        "author",
        "content",
        "created_at",
    )

    list_filter = (
        "lesson",
        "author",
    )

    search_fields = (
        "content",
        "author__username",
        "lesson__topic",
    )

    def has_add_permission(self, request):
        return request.user.is_superuser or request.user.role == "admin"

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.role == "admin"

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.role == "admin"

    def has_view_permission(self, request, obj=None):
        return request.user.is_authenticated
