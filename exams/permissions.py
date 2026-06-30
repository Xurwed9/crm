from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import BasePermission


class CanViewExam(BasePermission):
    message = _("You do not have permission to view exams.")

    def has_permission(self, request, view):
        return request.user.is_authenticated


class CanCreateExam(BasePermission):
    message = _("You do not have permission to create exams.")

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ["admin", "teacher"]


class CanEditExam(BasePermission):
    message = _("You do not have permission to edit exams.")

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ["admin", "teacher"]


class CanDeleteExam(BasePermission):
    message = _("You do not have permission to delete exams.")

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "admin"


class CanViewExamResult(BasePermission):
    message = _("You do not have permission to view exam results.")

    def has_permission(self, request, view):
        return request.user.is_authenticated


class CanCreateExamResult(BasePermission):
    message = _("You do not have permission to create exam results.")

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ["admin", "teacher"]


class CanEditExamResult(BasePermission):
    message = _("You do not have permission to edit exam results.")

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ["admin", "teacher"]


class CanDeleteExamResult(BasePermission):
    message = _("You do not have permission to delete exam results.")

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "admin"
