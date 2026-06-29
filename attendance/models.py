from django.db import models
from accounts.models import User
from students.models import Student
from groups.models import Group


class Attendance(models.Model):

    STATUS_CHOICES = (
        ("present", "Present"),
        ("absent", "Absent"),
        ("late", "Late"),
        ("excused", "Excused"),
    )

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="attendances",
    )

    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name="attendances",
    )

    teacher = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="recorded_attendances",
        limit_choices_to={"role": "teacher"},
    )

    date = models.DateField()

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="present",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        unique_together = ["student", "group", "date"]
        ordering = ["-date", "-id"]

    def __str__(self):

        return f"{self.student} - {self.date} - {self.get_status_display()}"
