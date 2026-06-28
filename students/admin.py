from django.contrib import admin
from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "first_name",
        "last_name",
        "user",
        "status",
    )


    search_fields = (
        "first_name",
        "last_name",
        "user__username",
        "user__phone_number",
    )


    list_filter = (
        "status",
    )