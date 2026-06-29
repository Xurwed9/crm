from django.contrib import admin
from .models import Grade


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "lesson",
        "student",
        "grade",
        "teacher",
        "created_at",
    )

    list_filter = (
        "lesson__group",
        "lesson__course",
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
