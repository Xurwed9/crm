from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    message = _("Only administrators can perform this action.")

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == "admin"
        )


class IsTeacher(BasePermission):
    message = _("Only teachers can perform this action.")

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == "teacher"
        )


class IsStudent(BasePermission):
    message = _("Only students can perform this action.")

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == "student"
        )


class IsAdminOrTeacher(BasePermission):
    message = _("Only administrators and teachers can perform this action.")

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role in ["admin", "teacher"]
        )


class IsOwner(BasePermission):
    message = _("You can only access your own data.")

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, "user"):
            return obj.user == request.user
        return obj == request.user
