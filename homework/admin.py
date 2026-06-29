from django.contrib import admin
from .models import Homework, Submission


@admin.register(Homework)
class HomeworkAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "lesson",
        "title",
        "deadline",
        "created_at",
    )

    search_fields = (
        "title",
        "lesson__topic",
    )

    list_filter = (
        "deadline",
        "lesson__group",
    )

    def has_add_permission(self, request):
        return request.user.is_superuser or request.user.role == "admin"

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.role == "admin"

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.role == "admin"

    def has_view_permission(self, request, obj=None):
        return request.user.is_authenticated


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "homework",
        "student",
        "grade",
        "submitted_at",
        "graded_at",
    )

    list_filter = (
        "homework",
        "grade",
    )

    search_fields = (
        "student__first_name",
        "student__last_name",
    )

    def has_add_permission(self, request):
        return request.user.is_superuser or request.user.role == "admin"

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.role == "admin"

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.role == "admin"

    def has_view_permission(self, request, obj=None):
        return request.user.is_authenticated
