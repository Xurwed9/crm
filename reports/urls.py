from django.urls import path
from .views import (
    AttendanceReportView,
    StudentReportView,
    TeacherReportView,
    PaymentReportView,
    MonthlyReportView,
)

urlpatterns = [
    path("attendance/", AttendanceReportView.as_view(), name="report-attendance"),
    path("students/", StudentReportView.as_view(), name="report-students"),
    path("teachers/", TeacherReportView.as_view(), name="report-teachers"),
    path("payments/", PaymentReportView.as_view(), name="report-payments"),
    path("monthly/", MonthlyReportView.as_view(), name="report-monthly"),
]
