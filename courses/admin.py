from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Course


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "price",
        "duration",
        "is_active",
        "created_at",
    )

    list_filter = (
        "is_active",
        "created_at",
    )

    search_fields = (
        "name",
        "description",
    )

    ordering = ("-id",)

    list_per_page = 10

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (_("Course Information"), {
            "fields": (
                "name",
                "description",
            ),
        }),
        (_("Course Details"), {
            "fields": (
                "price",
                "duration",
                "is_active",
            ),
        }),
        (_("System Information"), {
            "fields": (
                "created_at",
                "updated_at",
            ),
        }),
    )
