from django.contrib import admin
from .models import Exam, ExamResult


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "title",
        "lesson",
        "maximum_score",
        "passing_score",
        "date",
        "created_at",
    )

    list_filter = (
        "date",
        "lesson__group",
        "lesson__course",
    )

    search_fields = (
        "title",
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


@admin.register(ExamResult)
class ExamResultAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "exam",
        "student",
        "score",
        "created_at",
    )

    list_filter = (
        "exam",
        "exam__date",
    )

    search_fields = (
        "student__first_name",
        "student__last_name",
        "exam__title",
    )

    def has_add_permission(self, request):
        return request.user.is_superuser or request.user.role == "admin"

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.role == "admin"

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.role == "admin"

    def has_view_permission(self, request, obj=None):
        return request.user.is_authenticated
