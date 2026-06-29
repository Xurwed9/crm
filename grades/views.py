from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    UpdateAPIView,
    DestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.filters import SearchFilter

from .models import Grade
from .serializers import (
    GradeListSerializer,
    GradeDetailSerializer,
    GradeCreateUpdateSerializer,
)
from .permissions import (
    CanViewGrade,
    CanCreateGrade,
    CanEditGrade,
    CanDeleteGrade,
)


class GradeListAPIView(ListAPIView):
    """
    GET /api/grades/grades/

    Returns a list of grade records.

    Searchable fields: student name, group name, course name, lesson name.
    Queries are optimized with select_related() to avoid N+1 queries.

    Role-based filtering:
      - Admin:   sees all grade records
      - Teacher: sees only grades for groups they teach
      - Student: sees only their own grades
    """

    serializer_class = GradeListSerializer
    permission_classes = [IsAuthenticated, CanViewGrade]
    filter_backends = [SearchFilter]
    search_fields = [
        "student__first_name",
        "student__last_name",
        "group__name",
        "course__name",
        "lesson_name",
    ]

    def get_queryset(self):
        """
        Return grade records filtered by the user's role.

        select_related() fetches related student, teacher, group, and course
        data in a single database query for better performance.
        """

        user = self.request.user

        queryset = Grade.objects.select_related(
            "student",
            "teacher",
            "group",
            "course",
        )

        if user.role == "admin":
            return queryset

        if user.role == "teacher":
            # Teacher sees only grades for groups they teach
            return queryset.filter(group__teacher=user)

        if user.role == "student":
            # Student sees only their own grades
            return queryset.filter(student__user=user)

        return Grade.objects.none()


class GradeDetailAPIView(RetrieveAPIView):
    """
    GET /api/grades/grades/<id>/

    Returns a single grade record with full details.
    Object-level permission checking prevents unauthorized access.
    """

    serializer_class = GradeDetailSerializer
    permission_classes = [IsAuthenticated, CanViewGrade]

    def get_queryset(self):
        """
        Load all grade records with related data.
        The CanViewGrade permission's has_object_permission()
        will check whether the current user can see the requested record.
        """

        return Grade.objects.select_related(
            "student",
            "teacher",
            "group",
            "course",
        )


class GradeCreateAPIView(CreateAPIView):
    """
    POST /api/grades/grades/create/

    Creates a new grade record.

    - Admin:   can create for any group/course
    - Teacher: can create for their own groups (teacher auto-assigned)
    - Student: not allowed
    """

    serializer_class = GradeCreateUpdateSerializer
    permission_classes = [IsAuthenticated, CanCreateGrade]

    def perform_create(self, serializer):
        """
        When a teacher creates a grade record, automatically
        set the teacher field to the currently logged-in teacher.
        Admin users can specify any teacher in the request body.
        """

        user = self.request.user

        if user.role == "teacher":
            # Auto-assign the teacher field to the current user
            serializer.save(teacher=user)
        else:
            serializer.save()


class GradeUpdateAPIView(UpdateAPIView):
    """
    PATCH /api/grades/grades/<id>/update/

    Updates an existing grade record.

    - Admin:   can update any record
    - Teacher: can update records of groups they teach
    - Student: not allowed
    """

    serializer_class = GradeCreateUpdateSerializer
    permission_classes = [IsAuthenticated, CanEditGrade]
    http_method_names = ["patch"]

    def get_queryset(self):
        return Grade.objects.select_related(
            "student",
            "teacher",
            "group",
            "course",
        )


class GradeDeleteAPIView(DestroyAPIView):
    """
    DELETE /api/grades/grades/<id>/delete/

    Deletes a grade record.

    Only admin users can delete grade records.
    Teachers and students do not have this permission.
    """

    permission_classes = [IsAuthenticated, CanDeleteGrade]

    def get_queryset(self):
        return Grade.objects.select_related(
            "student",
            "teacher",
            "group",
            "course",
        )

    def destroy(self, request, *args, **kwargs):
        """
        Delete the record and return a friendly success message.
        """

        grade = self.get_object()
        grade.delete()

        return Response(
            {"detail": "Grade record deleted successfully."},
            status=status.HTTP_200_OK,
        )
