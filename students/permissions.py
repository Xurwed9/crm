from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import BasePermission


class IsAdminOrTeacher(BasePermission):
    message = _("Only administrators can modify this resource.")

    def has_permission(self, request, view):

        if not request.user.is_authenticated:
            return False

        if request.method in ["POST", "PUT", "PATCH", "DELETE"]:
            return request.user.role in ["admin"]

        return True
