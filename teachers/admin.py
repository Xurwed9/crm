from django.contrib import admin
from .models import Teacher


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "first_name",
        "last_name",
        "user",
        "speciality",
        "status",
    )

    search_fields = (
        "first_name",
        "last_name",
        "user__username",
        "user__phone_number",
        "speciality",
    )

    list_filter = (
        "status",
    )
