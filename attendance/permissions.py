from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import BasePermission


class CanViewAttendance(BasePermission):
    message = _("You do not have permission to view attendance records.")

    def has_permission(self, request, view):
        return request.user.is_authenticated


class CanCreateAttendance(BasePermission):
    message = _("You do not have permission to create attendance records.")

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ["admin", "teacher"]


class CanEditAttendance(BasePermission):
    message = _("You do not have permission to edit attendance records.")

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ["admin", "teacher"]


class CanDeleteAttendance(BasePermission):
    message = _("You do not have permission to delete attendance records.")

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "admin"
