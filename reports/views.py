from datetime import date, datetime

from django.db.models import Count, Sum, Q, Value, DecimalField
from django.db.models.functions import Coalesce
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import User
from students.models import Student
from teachers.models import Teacher
from groups.models import Group
from lessons.models import Lesson
from attendance.models import Attendance
from grades.models import Grade
from payments.models import Payment

from .utils import export_response


class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == "admin"
        )


class BaseReportView(APIView):

    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        fmt = request.query_params.get("format", "json")
        data, columns, filename = self.get_data(request)
        if fmt != "json":
            response = export_response(data, fmt, filename, columns)
            if response:
                return response
        return Response({"report": filename, "columns": columns, "rows": data})

    def get_data(self, request):
        raise NotImplementedError


class AttendanceReportView(BaseReportView):

    def get_data(self, request):

        qs = Attendance.objects.select_related(
            "student", "student__user", "lesson", "lesson__group",
        )

        group_id = request.query_params.get("group_id")
        student_id = request.query_params.get("student_id")
        date_from = request.query_params.get("date_from")
        date_to = request.query_params.get("date_to")
        lesson_id = request.query_params.get("lesson_id")

        if group_id:
            qs = qs.filter(lesson__group_id=group_id)
        if student_id:
            qs = qs.filter(student_id=student_id)
        if lesson_id:
            qs = qs.filter(lesson_id=lesson_id)
        if date_from:
            qs = qs.filter(lesson__lesson_date__gte=date_from)
        if date_to:
            qs = qs.filter(lesson__lesson_date__lte=date_to)

        columns = ["Student", "Group", "Date", "Lesson", "Status"]
        rows = [
            [
                str(a.student),
                a.lesson.group.name,
                a.lesson.lesson_date,
                a.lesson.topic,
                a.get_status_display(),
            ]
            for a in qs
        ]

        return rows, columns, "attendance_report"


class StudentReportView(BaseReportView):

    def get_data(self, request):

        group_id = request.query_params.get("group_id")
        status_filter = request.query_params.get("status")

        qs = Student.objects.select_related("user")

        if group_id:
            qs = qs.filter(groups__id=group_id)
        if status_filter:
            qs = qs.filter(status=status_filter)

        qs = qs.annotate(
            total_attendance=Count("attendances"),
            present_count=Count(
                "attendances", filter=Q(attendances__status="present"),
            ),
            absent_count=Count(
                "attendances", filter=Q(attendances__status="absent"),
            ),
            late_count=Count(
                "attendances", filter=Q(attendances__status="late"),
            ),
            avg_grade=Coalesce(
                Sum("grades__grade") * 1.0 / Count("grades"),
                Value(0),
                output_field=DecimalField(max_digits=5, decimal_places=1),
            ),
            total_paid=Coalesce(
                Sum(
                    "payments__amount",
                    filter=Q(payments__status="paid"),
                ),
                Value(0, output_field=DecimalField(max_digits=10, decimal_places=2)),
            ),
        )

        columns = [
            "Student", "Group", "Total", "Present",
            "Absent", "Late", "Avg Grade", "Total Paid",
        ]
        rows = [
            [
                str(s),
                ", ".join(g.name for g in s.groups.all()),
                s.total_attendance,
                s.present_count,
                s.absent_count,
                s.late_count,
                s.avg_grade,
                s.total_paid,
            ]
            for s in qs
        ]

        return rows, columns, "student_report"


class TeacherReportView(BaseReportView):

    def get_data(self, request):

        qs = Teacher.objects.select_related("user")

        status_filter = request.query_params.get("status")
        if status_filter:
            qs = qs.filter(status=status_filter)

        qs = qs.annotate(
            groups_count=Count("user__teaching_groups", distinct=True),
            lessons_count=Count("user__lessons", distinct=True),
        )

        columns = ["Teacher", "Speciality", "Groups", "Lessons", "Group Names"]
        rows = [
            [
                str(t),
                t.speciality,
                t.groups_count,
                t.lessons_count,
                ", ".join(
                    g.name for g in Group.objects.filter(teacher=t.user)
                ),
            ]
            for t in qs
        ]

        return rows, columns, "teacher_report"


class PaymentReportView(BaseReportView):

    def get_data(self, request):

        qs = Payment.objects.select_related("student", "student__user")

        student_id = request.query_params.get("student_id")
        status_filter = request.query_params.get("status")
        date_from = request.query_params.get("date_from")
        date_to = request.query_params.get("date_to")

        if student_id:
            qs = qs.filter(student_id=student_id)
        if status_filter:
            qs = qs.filter(status=status_filter)
        if date_from:
            qs = qs.filter(paid_date__gte=date_from)
        if date_to:
            qs = qs.filter(paid_date__lte=date_to)

        columns = ["Student", "Amount", "Discount", "Net", "Date", "Method", "Status"]
        rows = [
            [
                str(p.student),
                float(p.amount),
                float(p.discount),
                float(p.amount - p.discount),
                p.paid_date,
                p.get_payment_method_display(),
                p.get_status_display(),
            ]
            for p in qs
        ]

        return rows, columns, "payment_report"


class MonthlyReportView(BaseReportView):

    def get_data(self, request):

        year = int(request.query_params.get("year", date.today().year))

        columns = [
            "Month", "New Students", "Lessons", "Present",
            "Absent", "Late", "Income",
        ]
        rows = []

        for mo in range(1, 13):

            new_students = User.objects.filter(
                role="student",
                date_joined__year=year,
                date_joined__month=mo,
            ).count()

            lessons = Lesson.objects.filter(
                lesson_date__year=year,
                lesson_date__month=mo,
            ).count()

            present = Attendance.objects.filter(
                lesson__lesson_date__year=year,
                lesson__lesson_date__month=mo,
                status="present",
            ).count()

            absent = Attendance.objects.filter(
                lesson__lesson_date__year=year,
                lesson__lesson_date__month=mo,
                status="absent",
            ).count()

            late = Attendance.objects.filter(
                lesson__lesson_date__year=year,
                lesson__lesson_date__month=mo,
                status="late",
            ).count()

            income = Payment.objects.filter(
                status="paid",
                paid_date__year=year,
                paid_date__month=mo,
            ).aggregate(
                total=Coalesce(
                    Sum("amount"),
                    Value(0, output_field=DecimalField(max_digits=10, decimal_places=2)),
                ),
            )["total"]

            month_name = datetime(year, mo, 1).strftime("%B")
            rows.append([
                f"{month_name} {year}", new_students, lessons,
                present, absent, late, float(income),
            ])

        return rows, columns, "monthly_report"
