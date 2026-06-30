from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Lesson


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "group",
        "course",
        "lesson_number",
        "topic",
        "lesson_date",
        "start_time",
        "end_time",
        "lesson_type",
        "status",
        "teacher",
    )

    list_filter = (
        "status",
        "lesson_type",
        "lesson_date",
        "group",
        "course",
    )

    search_fields = (
        "topic",
        "group__name",
        "course__name",
    )

    date_hierarchy = "lesson_date"

    def has_add_permission(self, request):
        return request.user.is_superuser or request.user.role == "admin"

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.role == "admin"

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.role == "admin"

    def has_view_permission(self, request, obj=None):
        return request.user.is_authenticated
