from django.contrib import admin
from .models import Attendance


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    """
    Admin interface for managing Attendance records in the Django admin panel.

    Only users with the 'admin' role can create, edit, or delete attendance
    records through the admin panel. All authenticated users can view them.
    """

    # Columns shown in the attendance list view
    list_display = (
        "id",
        "student",
        "group",
        "teacher",
        "date",
        "status",
        "created_at",
    )

    # Filters available in the sidebar
    list_filter = (
        "status",
        "date",
        "group",
    )

    # Fields that can be searched
    search_fields = (
        "student__first_name",
        "student__last_name",
        "group__name",
        "date",
    )

    # Adds a date drill-down navigation
    date_hierarchy = "date"

    def has_add_permission(self, request):
        """Only admin users can add attendance records."""
        return request.user.is_superuser or request.user.role == "admin"

    def has_change_permission(self, request, obj=None):
        """Only admin users can edit attendance records."""
        return request.user.is_superuser or request.user.role == "admin"

    def has_delete_permission(self, request, obj=None):
        """Only admin users can delete attendance records."""
        return request.user.is_superuser or request.user.role == "admin"

    def has_view_permission(self, request, obj=None):
        """All authenticated users can view attendance records."""
        return request.user.is_authenticated
