from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import BasePermission


class CanViewJournal(BasePermission):
    message = _("You do not have permission to view the journal.")

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):

        user = request.user

        if user.role == "admin":
            return True

        if user.role == "teacher":
            return obj.teacher == user or obj.group.teacher == user

        if user.role == "student":
            return obj.group.students.filter(user=user).exists()

        return False


class CanCreateJournalComment(BasePermission):
    message = _("You do not have permission to create journal comments.")

    def has_permission(self, request, view):
        return request.user.is_authenticated


class CanEditJournalComment(BasePermission):
    message = _("You do not have permission to edit journal comments.")

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):

        user = request.user

        if user.role == "admin":
            return True

        return obj.author == user


class CanDeleteJournalComment(BasePermission):
    message = _("You do not have permission to delete journal comments.")

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == "admin"
        )
