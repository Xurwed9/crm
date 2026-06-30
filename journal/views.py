from rest_framework import status
from rest_framework.generics import (
    RetrieveAPIView,
    ListAPIView,
    CreateAPIView,
    UpdateAPIView,
    DestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Prefetch

from lessons.models import Lesson
from attendance.models import Attendance
from grades.models import Grade
from homework.models import Homework, Submission
from exams.models import Exam, ExamResult

from .models import JournalComment
from .serializers import (
    JournalCommentListSerializer,
    JournalCommentDetailSerializer,
    JournalCommentCreateSerializer,
)
from .permissions import (
    CanViewJournal,
    CanCreateJournalComment,
    CanEditJournalComment,
    CanDeleteJournalComment,
)


class JournalDetailAPIView(RetrieveAPIView):

    permission_classes = [IsAuthenticated, CanViewJournal]

    def get_object(self):

        lesson = Lesson.objects.select_related(
            "group",
            "course",
            "teacher",
        ).prefetch_related(
            Prefetch(
                "attendances",
                queryset=Attendance.objects.select_related(
                    "student",
                    "student__user",
                ),
            ),
            Prefetch(
                "grades",
                queryset=Grade.objects.select_related(
                    "student",
                    "student__user",
                    "teacher",
                ),
            ),
            Prefetch(
                "homeworks",
                queryset=Homework.objects.prefetch_related(
                    Prefetch(
                        "submissions",
                        queryset=Submission.objects.select_related(
                            "student",
                            "student__user",
                        ),
                    ),
                ),
            ),
            Prefetch(
                "exams",
                queryset=Exam.objects.prefetch_related(
                    Prefetch(
                        "results",
                        queryset=ExamResult.objects.select_related(
                            "student",
                            "student__user",
                        ),
                    ),
                ),
            ),
            Prefetch(
                "journal_comments",
                queryset=JournalComment.objects.select_related(
                    "author",
                ),
            ),
        ).get(pk=self.kwargs["pk"])

        return lesson

    def retrieve(self, request, *args, **kwargs):

        lesson = self.get_object()
        user = request.user

        lesson_data = {
            "id": lesson.id,
            "lesson_number": lesson.lesson_number,
            "lesson_date": lesson.lesson_date,
            "start_time": lesson.start_time,
            "end_time": lesson.end_time,
            "topic": lesson.topic,
            "description": lesson.description,
            "lesson_type": lesson.lesson_type,
            "lesson_type_display": lesson.get_lesson_type_display(),
            "status": lesson.status,
            "status_display": lesson.get_status_display(),
            "group": str(lesson.group),
            "course": str(lesson.course),
            "teacher": str(lesson.teacher) if lesson.teacher else None,
        }

        attendance_data = []
        for att in lesson.attendances.all():
            if user.role == "student" and att.student.user != user:
                continue
            attendance_data.append({
                "id": att.id,
                "student_id": att.student.id,
                "student_name": str(att.student),
                "status": att.status,
                "status_display": att.get_status_display(),
                "reason": att.reason,
                "comment": att.comment,
            })

        grades_data = []
        for grade in lesson.grades.all():
            if user.role == "student" and grade.student.user != user:
                continue
            grades_data.append({
                "id": grade.id,
                "student_id": grade.student.id,
                "student_name": str(grade.student),
                "grade": grade.grade,
                "comment": grade.comment,
            })

        homeworks_data = []
        for homework in lesson.homeworks.all():
            submissions_data = []
            for sub in homework.submissions.all():
                if user.role == "student" and sub.student.user != user:
                    continue
                submissions_data.append({
                    "id": sub.id,
                    "student_id": sub.student.id,
                    "student_name": str(sub.student),
                    "grade": sub.grade,
                    "feedback": sub.feedback,
                    "submitted_at": sub.submitted_at,
                    "graded_at": sub.graded_at,
                })
            homeworks_data.append({
                "id": homework.id,
                "title": homework.title,
                "description": homework.description,
                "deadline": homework.deadline,
                "submissions": submissions_data,
            })

        exam_data = None
        exam_obj = lesson.exams.first()
        if exam_obj:
            results_data = []
            for result in exam_obj.results.all():
                if user.role == "student" and result.student.user != user:
                    continue
                results_data.append({
                    "id": result.id,
                    "student_id": result.student.id,
                    "student_name": str(result.student),
                    "score": result.score,
                    "comment": result.comment,
                })
            exam_data = {
                "id": exam_obj.id,
                "title": exam_obj.title,
                "description": exam_obj.description,
                "maximum_score": exam_obj.maximum_score,
                "passing_score": exam_obj.passing_score,
                "date": exam_obj.date,
                "results": results_data,
            }

        comments_data = []
        for comment in lesson.journal_comments.all():
            if user.role == "student":
                if comment.author.role == "student" and comment.author != user:
                    continue
            comments_data.append({
                "id": comment.id,
                "author": str(comment.author),
                "author_role": comment.author.role,
                "content": comment.content,
                "created_at": comment.created_at,
            })

        return Response({
            "lesson": lesson_data,
            "attendance": attendance_data,
            "grades": grades_data,
            "homeworks": homeworks_data,
            "exam": exam_data,
            "comments": comments_data,
        })


class JournalCommentListAPIView(ListAPIView):

    serializer_class = JournalCommentListSerializer
    permission_classes = [IsAuthenticated, CanViewJournal]

    def get_queryset(self):

        lesson = Lesson.objects.get(pk=self.kwargs["lesson_pk"])
        user = self.request.user

        if user.role == "admin":
            return JournalComment.objects.filter(lesson=lesson).select_related("author")

        if user.role == "teacher":
            return JournalComment.objects.filter(lesson=lesson).select_related("author")

        if user.role == "student":
            return JournalComment.objects.filter(
                lesson=lesson,
            ).select_related("author")

        return JournalComment.objects.none()


class JournalCommentCreateAPIView(CreateAPIView):

    serializer_class = JournalCommentCreateSerializer
    permission_classes = [IsAuthenticated, CanCreateJournalComment]

    def perform_create(self, serializer):

        lesson = Lesson.objects.get(pk=self.kwargs["lesson_pk"])

        user = self.request.user

        if user.role == "teacher" and lesson.teacher != user and lesson.group.teacher != user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied(
                "You can only comment on your own lessons."
            )

        if user.role == "student" and not lesson.group.students.filter(user=user).exists():
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied(
                "You can only comment on your own lessons."
            )

        serializer.save(
            lesson=lesson,
            author=user,
        )


class JournalCommentUpdateAPIView(UpdateAPIView):

    serializer_class = JournalCommentCreateSerializer
    permission_classes = [IsAuthenticated, CanEditJournalComment]
    http_method_names = ["patch"]

    def get_queryset(self):
        return JournalComment.objects.select_related("author")


class JournalCommentDeleteAPIView(DestroyAPIView):

    permission_classes = [IsAuthenticated, CanDeleteJournalComment]

    def get_queryset(self):
        return JournalComment.objects.select_related("author")

    def destroy(self, request, *args, **kwargs):

        comment = self.get_object()
        comment.delete()

        return Response(
            {"detail": "Comment deleted successfully."},
            status=status.HTTP_200_OK,
        )
