from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Payment, PaymentHistory, StudentDebt


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "student",
        "amount",
        "discount",
        "paid_date",
        "payment_method",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "payment_method",
        "paid_date",
    )

    search_fields = (
        "student__first_name",
        "student__last_name",
        "comment",
    )

    def has_add_permission(self, request):
        return request.user.is_superuser or request.user.role == "admin"

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.role == "admin"

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.role == "admin"

    def has_view_permission(self, request, obj=None):
        return request.user.is_authenticated


@admin.register(PaymentHistory)
class PaymentHistoryAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "payment",
        "action",
        "changed_at",
    )

    list_filter = (
        "action",
        "changed_at",
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.role == "admin"

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.role == "admin"


@admin.register(StudentDebt)
class StudentDebtAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "student",
        "total_fees",
        "updated_at",
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
        return request.user.is_superuser or request.user.role == "admin"
