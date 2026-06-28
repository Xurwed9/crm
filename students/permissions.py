from rest_framework.permissions import BasePermission


class IsAdminOrTeacher(BasePermission):

    def has_permission(self, request, view):

        if not request.user.is_authenticated:
            return False

        if request.method in ["POST", "PUT", "PATCH", "DELETE"]:
            return request.user.role in ["admin"]

        return True