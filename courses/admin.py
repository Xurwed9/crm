from django.contrib import admin

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

    ordering = (
        "-id",
    )

    list_per_page = 10

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (
        ("Course Information", {
            "fields": (
                "name",
                "description",
            ),
        }),

        ("Course Details", {
            "fields": (
                "price",
                "duration",
                "is_active",
            ),
        }),

        ("System Information", {
            "fields": (
                "created_at",
                "updated_at",
            ),
        }),
    )