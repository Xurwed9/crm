from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == "admin"
        )


class CanViewAttendance(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):

        user = request.user

        if user.role == "admin":
            return True

        if user.role == "teacher":
            return obj.group.teacher == user

        if user.role == "student":
            return obj.student.user == user

        return False


class CanCreateAttendance(BasePermission):

    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated:
            return False

        return user.role in ["admin", "teacher"]


class CanEditAttendance(BasePermission):


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
            return obj.group.teacher == user

        return False


class CanDeleteAttendance(BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == "admin"
        )
