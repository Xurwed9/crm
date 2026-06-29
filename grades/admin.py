from django.contrib import admin
from .models import Grade


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    """
    Admin interface for managing Grade records in the Django admin panel.

    Only users with the 'admin' role can create, edit, or delete grade
    records through the admin panel. All authenticated users can view them.
    """

    # Columns shown in the grade list view
    list_display = (
        "id",
        "student",
        "group",
        "course",
        "lesson_name",
        "grade",
        "teacher",
        "created_at",
    )

    # Filters available in the sidebar
    list_filter = (
        "course",
        "group",
    )

    # Fields that can be searched
    search_fields = (
        "student__first_name",
        "student__last_name",
        "group__name",
        "course__name",
        "lesson_name",
    )

    def has_add_permission(self, request):
        """Only admin users can add grade records."""
        return request.user.is_superuser or request.user.role == "admin"

    def has_change_permission(self, request, obj=None):
        """Only admin users can edit grade records."""
        return request.user.is_superuser or request.user.role == "admin"

    def has_delete_permission(self, request, obj=None):
        """Only admin users can delete grade records."""
        return request.user.is_superuser or request.user.role == "admin"

    def has_view_permission(self, request, obj=None):
        """All authenticated users can view grade records."""
        return request.user.is_authenticated
