from django.contrib import admin
from django.utils.translation import gettext_lazy as _

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
