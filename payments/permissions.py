from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import BasePermission


class CanViewPayment(BasePermission):
    message = _("You do not have permission to view payments.")

    def has_permission(self, request, view):
        return request.user.is_authenticated


class CanCreatePayment(BasePermission):
    message = _("You do not have permission to create payments.")

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "admin"


class CanEditPayment(BasePermission):
    message = _("You do not have permission to edit payments.")

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "admin"


class CanDeletePayment(BasePermission):
    message = _("You do not have permission to delete payments.")

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "admin"


class CanViewPaymentHistory(BasePermission):
    message = _("You do not have permission to view payment history.")

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "admin"
