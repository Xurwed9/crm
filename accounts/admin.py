from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)

    list_display = (
        "id",
        "username",
        "phone_number",
        "role",
        "is_active",
        "is_staff",
    )

    search_fields = (
        "username",
        "phone_number",
        "email",
    )

    list_filter = (
        "role",
        "is_active",
        "is_staff",
    )

    ordering = ("-id",)

    fieldsets = BaseUserAdmin.fieldsets + (
        (
            "Additional Information",
            {
                "fields": (
                    "phone_number",
                    "role",
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (
            "Additional Information",
            {
                "fields": (
                    "phone_number",
                    "role",
                )
            },
        ),
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "image",
        "address",
        "birth_date",
    )

    search_fields = (
        "user__username",
        "user__phone_number",
    )

    ordering = ("-id",)
