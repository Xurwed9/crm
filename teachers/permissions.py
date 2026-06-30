from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    message = _("Only administrators can perform this action.")

    def has_permission(self, request, view):

        if not request.user.is_authenticated:
            return False

        return request.user.role == "admin"
