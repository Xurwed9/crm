from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Attendance


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "lesson",
        "student",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "lesson__lesson_date",
        "lesson__group",
    )

    search_fields = (
        "student__first_name",
        "student__last_name",
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
