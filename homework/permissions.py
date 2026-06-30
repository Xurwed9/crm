from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    message = _("You do not have permission to access this resource.")

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == "admin"
        )

class CanViewHomework(BasePermission):
    message = _("You do not have permission to view homework.")

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):

        user = request.user

        if user.role == "admin":
            return True

        if user.role == "teacher":
            return obj.lesson.teacher == user

        if user.role == "student":
            return obj.lesson.group.students.filter(user=user).exists()

        return False


class CanCreateHomework(BasePermission):
    message = _("You do not have permission to create homework.")

    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated:
            return False

        return user.role in ["admin", "teacher"]


class CanEditHomework(BasePermission):
    message = _("You do not have permission to edit homework.")

    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated:
            return False

        return user.role in ["admin", "teacher"]

    def has_object_permission(self, request, view, obj):

        user = request.user

        if user.role == "admin":
            return True

        if user.role == "teacher":
            return obj.lesson.teacher == user

        return False


class CanDeleteHomework(BasePermission):
    message = _("You do not have permission to delete homework.")

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == "admin"
        )


class CanViewSubmission(BasePermission):
    message = _("You do not have permission to view submissions.")

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):

        user = request.user

        if user.role == "admin":
            return True

        if user.role == "teacher":
            return obj.homework.lesson.teacher == user

        if user.role == "student":
            return obj.student.user == user

        return False


class CanCreateSubmission(BasePermission):
    message = _("You do not have permission to create submissions.")

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == "student"
        )


class CanGradeSubmission(BasePermission):
    message = _("You do not have permission to grade submissions.")

    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated:
            return False

        return user.role in ["admin", "teacher"]

    def has_object_permission(self, request, view, obj):

        user = request.user

        if user.role == "admin":
            return True

        if user.role == "teacher":
            return obj.homework.lesson.teacher == user

        return False


class CanDeleteSubmission(BasePermission):
    message = _("You do not have permission to delete submissions.")

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == "admin"
        )
