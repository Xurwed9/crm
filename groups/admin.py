from django.contrib import admin
from .models import Group


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "course",
        "teacher",
        "status",
        "start_date",
        "end_date",
    )

    list_filter = (
        "status",
        "course",
        "teacher",
    )

    search_fields = (
        "name",
        "course__name",
        "teacher__username",
        "teacher__first_name",
        "teacher__last_name",
    )

    ordering = ("-id",)

    list_per_page = 10

    autocomplete_fields = (
        "course",
        "teacher",
    )