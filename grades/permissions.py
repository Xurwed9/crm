from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import BasePermission


class CanViewGrade(BasePermission):
    message = _("You do not have permission to view grades.")

    def has_permission(self, request, view):
        return request.user.is_authenticated


class CanCreateGrade(BasePermission):
    message = _("You do not have permission to create grades.")

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ["admin", "teacher"]


class CanEditGrade(BasePermission):
    message = _("You do not have permission to edit grades.")

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ["admin", "teacher"]


class CanDeleteGrade(BasePermission):
    message = _("You do not have permission to delete grades.")

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "admin"
