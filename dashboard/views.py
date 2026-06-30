from datetime import date

from django.utils.translation import gettext_lazy as _
from django.db.models import (
    Count, Sum, Q, Value, OuterRef, Subquery,
    DecimalField, F, Prefetch,
)
from django.db.models.functions import Coalesce
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from students.models import Student
from teachers.models import Teacher
from groups.models import Group
from courses.models import Course
from lessons.models import Lesson
from attendance.models import Attendance
from grades.models import Grade
from homework.models import Homework, Submission
from payments.models import Payment, StudentDebt


class DashboardAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        user = request.user

        if user.role == "admin":
            data = self._admin_dashboard()

        elif user.role == "teacher":
            data = self._teacher_dashboard(user)

        elif user.role == "student":
            data = self._student_dashboard(user)

        else:
            data = {}

        return Response(data)

    def _admin_dashboard(self):

        today = date.today()

        total_students = Student.objects.count()
        total_teachers = Teacher.objects.count()
        active_groups = Group.objects.filter(status="active").count()
        total_courses = Course.objects.count()

        today_lessons = Lesson.objects.filter(
            lesson_date=today,
        ).select_related("group", "course")

        lessons_data = [
            {
                "id": l.id,
                "group": l.group.name,
                "course": l.course.name,
                "topic": l.topic,
                "start_time": l.start_time,
                "end_time": l.end_time,
                "status": l.status,
            }
            for l in today_lessons
        ]

        attendance_stats = Attendance.objects.filter(
            lesson__lesson_date=today,
        ).values("status").annotate(count=Count("id"))

        attendance_data = {"present": 0, "absent": 0, "late": 0, "excused": 0}
        for stat in attendance_stats:
            attendance_data[stat["status"]] = stat["count"]
        attendance_data["total"] = sum(attendance_data.values())

        income_total = Payment.objects.filter(
            status="paid",
        ).aggregate(
            total=Coalesce(
                Sum("amount"),
                Value(0, output_field=DecimalField(max_digits=10, decimal_places=2)),
            ),
        )["total"]

        income_this_month = Payment.objects.filter(
            status="paid",
            paid_date__year=today.year,
            paid_date__month=today.month,
        ).aggregate(
            total=Coalesce(
                Sum("amount"),
                Value(0, output_field=DecimalField(max_digits=10, decimal_places=2)),
            ),
        )["total"]

        total_fees_subq = StudentDebt.objects.filter(
            student=OuterRef("pk"),
        ).values("total_fees")[:1]

        debtors = Student.objects.annotate(
            total_fees=Coalesce(
                Subquery(total_fees_subq),
                Value(0),
                output_field=DecimalField(max_digits=10, decimal_places=2),
            ),
            paid_amount=Coalesce(
                Sum(
                    "payments__amount",
                    filter=Q(payments__status="paid"),
                ),
                Value(0),
                output_field=DecimalField(max_digits=10, decimal_places=2),
            ),
            total_discount=Coalesce(
                Sum(
                    "payments__discount",
                    filter=Q(payments__status="paid"),
                ),
                Value(0),
                output_field=DecimalField(max_digits=10, decimal_places=2),
            ),
        ).filter(total_fees__gt=0).annotate(
            remaining=F("total_fees") - F("paid_amount") - F("total_discount"),
        ).filter(remaining__gt=0)[:10]

        debtors_data = [
            {
                "student": str(d),
                "total_fees": d.total_fees,
                "paid": d.paid_amount,
                "total_discount": d.total_discount,
                "remaining": d.remaining,
            }
            for d in debtors
        ]

        return {
            "total_students": total_students,
            "total_teachers": total_teachers,
            "active_groups": active_groups,
            "total_courses": total_courses,
            "today_lessons": lessons_data,
            "today_attendance": attendance_data,
            "income": {
                "total": income_total,
                "this_month": income_this_month,
            },
            "debtors": debtors_data,
        }

    def _teacher_dashboard(self, user):

        today = date.today()

        today_lessons = Lesson.objects.filter(
            teacher=user,
            lesson_date=today,
        ).select_related("group", "course")

        lessons_data = [
            {
                "id": l.id,
                "group": l.group.name,
                "course": l.course.name,
                "topic": l.topic,
                "start_time": l.start_time,
                "end_time": l.end_time,
                "status": l.status,
            }
            for l in today_lessons
        ]

        own_groups = Group.objects.filter(
            teacher=user,
        ).annotate(
            student_count=Count("students"),
        ).select_related("course")

        groups_data = [
            {
                "id": g.id,
                "name": g.name,
                "course": g.course.name,
                "student_count": g.student_count,
            }
            for g in own_groups
        ]

        attendance_stats = Attendance.objects.filter(
            lesson__teacher=user,
            lesson__lesson_date=today,
        ).values("status").annotate(count=Count("id"))

        attendance_data = {"present": 0, "absent": 0, "late": 0, "excused": 0}
        for stat in attendance_stats:
            attendance_data[stat["status"]] = stat["count"]
        attendance_data["total"] = sum(attendance_data.values())

        total_homework = Homework.objects.filter(
            lesson__teacher=user,
        ).count()

        ungraded_submissions = Submission.objects.filter(
            homework__lesson__teacher=user,
            grade__isnull=True,
        ).count()

        return {
            "today_lessons": lessons_data,
            "own_groups": groups_data,
            "today_attendance": attendance_data,
            "homework": {
                "total": total_homework,
                "ungraded_submissions": ungraded_submissions,
            },
        }

    def _student_dashboard(self, user):

        today = date.today()
        try:
            student = user.student
        except Exception:
            return {"detail": _("Student profile not found.")}

        group = student.groups.select_related("course").first()
        group_data = None
        if group:
            group_data = {
                "id": group.id,
                "name": group.name,
                "course": group.course.name,
            }

        today_lesson = Lesson.objects.filter(
            group__students__user=user,
            lesson_date=today,
        ).select_related("group", "teacher").first()

        today_lesson_data = None
        if today_lesson:
            today_lesson_data = {
                "id": today_lesson.id,
                "topic": today_lesson.topic,
                "start_time": today_lesson.start_time,
                "end_time": today_lesson.end_time,
                "group": today_lesson.group.name,
                "teacher": (
                    f"{today_lesson.teacher.first_name} {today_lesson.teacher.last_name}"
                    if today_lesson.teacher else None
                ),
                "status": today_lesson.status,
            }

        attendance_records = Attendance.objects.filter(
            student=student,
        ).select_related("lesson")[:10]

        attendance_data = [
            {
                "date": a.lesson.lesson_date,
                "lesson": a.lesson.topic,
                "status": a.status,
            }
            for a in attendance_records
        ]

        grade_records = Grade.objects.filter(
            student=student,
        ).select_related("lesson")[:10]

        grades_data = [
            {
                "date": g.lesson.lesson_date,
                "lesson": g.lesson.topic,
                "grade": g.grade,
                "comment": g.comment,
            }
            for g in grade_records
        ]

        homework_records = Homework.objects.filter(
            lesson__group__students__user=user,
        ).prefetch_related(
            Prefetch(
                "submissions",
                queryset=Submission.objects.filter(student=student),
            ),
        )[:10]

        homework_data = []
        for hw in homework_records:
            sub = hw.submissions.all().first()
            homework_data.append({
                "id": hw.id,
                "title": hw.title,
                "deadline": hw.deadline,
                "submitted": sub is not None,
                "grade": sub.grade if sub else None,
                "feedback": sub.feedback if sub else None,
            })

        payment_records = Payment.objects.filter(
            student=student,
        )[:5]

        payments_data = [
            {
                "amount": p.amount,
                "discount": p.discount,
                "paid_date": p.paid_date,
                "payment_method": p.payment_method,
                "status": p.status,
            }
            for p in payment_records
        ]

        return {
            "group": group_data,
            "today_lesson": today_lesson_data,
            "attendance": attendance_data,
            "grades": grades_data,
            "homework": homework_data,
            "payments": payments_data,
        }
