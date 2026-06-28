from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == "admin"
        )


class IsTeacher(BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == "teacher"
        )


class IsStudent(BasePermission):
    """
    Танҳо Student.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == "student"
        )


class IsAdminOrTeacher(BasePermission):
    """
    Admin ё Teacher.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role in ["admin", "teacher"]
        )


class IsAdminOrReadOnly(BasePermission):
    """
    Ҳама хонда метавонанд.
    Танҳо Admin метавонад create/update/delete кунад.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return (
            request.user.is_authenticated
            and request.user.role == "admin"
        )


class IsTeacherOrReadOnly(BasePermission):
    """
    Ҳама хонда метавонанд.
    Танҳо Teacher метавонад edit кунад.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return (
            request.user.is_authenticated
            and request.user.role == "teacher"
        )