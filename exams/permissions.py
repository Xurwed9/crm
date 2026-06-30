from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == "admin"
        )


class CanViewExam(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):

        user = request.user

        if user.role == "admin":
            return True

        if user.role == "teacher":
            return obj.lesson.group.teacher == user

        if user.role == "student":
            return obj.lesson.group.students.filter(user=user).exists()

        return False


class CanCreateExam(BasePermission):

    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated:
            return False

        return user.role in ["admin", "teacher"]


class CanEditExam(BasePermission):

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
            return obj.lesson.group.teacher == user

        return False


class CanDeleteExam(BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == "admin"
        )


class CanViewExamResult(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):

        user = request.user

        if user.role == "admin":
            return True

        if user.role == "teacher":
            return obj.exam.lesson.group.teacher == user

        if user.role == "student":
            return obj.student.user == user

        return False


class CanCreateExamResult(BasePermission):

    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated:
            return False

        return user.role in ["admin", "teacher"]


class CanEditExamResult(BasePermission):

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
            return obj.exam.lesson.group.teacher == user

        return False


class CanDeleteExamResult(BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == "admin"
        )
