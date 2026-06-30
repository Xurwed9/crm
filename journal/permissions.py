from rest_framework.permissions import BasePermission


class CanViewJournal(BasePermission):

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

    def has_permission(self, request, view):
        return request.user.is_authenticated


class CanEditJournalComment(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):

        user = request.user

        if user.role == "admin":
            return True

        return obj.author == user


class CanDeleteJournalComment(BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == "admin"
        )
