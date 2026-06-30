from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == "admin"
        )


class CanViewPayment(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False
        return user.role in ["admin", "student"]

    def has_object_permission(self, request, view, obj):

        user = request.user

        if user.role == "admin":
            return True

        if user.role == "student":
            return obj.student.user == user

        return False


class CanCreatePayment(BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == "admin"
        )


class CanEditPayment(BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == "admin"
        )

    def has_object_permission(self, request, view, obj):
        return request.user.role == "admin"


class CanDeletePayment(BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == "admin"
        )


class CanViewPaymentHistory(BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == "admin"
        )
