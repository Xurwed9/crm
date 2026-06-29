from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """
    Grants access only to users with the 'admin' role.
    Used for delete operations and as a building block for other permissions.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == "admin"
        )


class CanViewGrade(BasePermission):
    """
    Controls who can view grade records.

    Rules:
      - Admin:   can view every grade record
      - Teacher: can view grades for groups they teach
      - Student: can view only their own grades
    """

    def has_permission(self, request, view):
        """All authenticated users may potentially view grades."""
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Check if a specific grade record can be viewed by the current user.

        This is called automatically by DRF for detail views (RetrieveAPIView).
        """

        user = request.user

        if user.role == "admin":
            return True

        if user.role == "teacher":
            # Teacher can only view grades for their own groups
            return obj.group.teacher == user

        if user.role == "student":
            # Student can only view their own grades
            return obj.student.user == user

        return False


class CanCreateGrade(BasePermission):
    """
    Controls who can create grade records.

    Rules:
      - Admin:   can create grades for any group
      - Teacher: can create grades (auto-assigned to their groups)
      - Student: cannot create grades
    """

    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated:
            return False

        return user.role in ["admin", "teacher"]


class CanEditGrade(BasePermission):
    """
    Controls who can edit grade records.

    Rules:
      - Admin:   can edit any grade record
      - Teacher: can edit grades of groups they teach
      - Student: cannot edit grades
    """

    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated:
            return False

        return user.role in ["admin", "teacher"]

    def has_object_permission(self, request, view, obj):
        """
        Check if a specific grade record can be edited.

        Used automatically by DRF for UpdateAPIView.
        """

        user = request.user

        if user.role == "admin":
            return True

        if user.role == "teacher":
            # Teacher can only edit grades for their own groups
            return obj.group.teacher == user

        return False


class CanDeleteGrade(BasePermission):
    """
    Controls who can delete grade records.

    Rules:
      - Admin:   can delete any grade record
      - Teacher: cannot delete grades
      - Student: cannot delete grades
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == "admin"
        )
