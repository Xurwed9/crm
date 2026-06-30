from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import BasePermission


class CanViewLesson(BasePermission):
    message = _("You do not have permission to view lessons.")

    def has_permission(self, request, view):
        return request.user.is_authenticated


class CanCreateLesson(BasePermission):
    message = _("You do not have permission to create lessons.")

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ["admin", "teacher"]


class CanEditLesson(BasePermission):
    message = _("You do not have permission to edit lessons.")

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ["admin", "teacher"]


class CanDeleteLesson(BasePermission):
    message = _("You do not have permission to delete lessons.")

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "admin"
