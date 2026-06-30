from django.db import models
from students.models import Student
from lessons.models import Lesson


class Attendance(models.Model):

    STATUS_CHOICES = (
        ("present", "Present"),
        ("absent", "Absent"),
        ("late", "Late"),
        ("excused", "Excused"),
    )

    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name="attendances",
    )

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="attendances",
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="present",
    )

    reason = models.TextField(
        blank=True,
    )

    comment = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        unique_together = ["lesson", "student"]
        ordering = ["-lesson__lesson_date", "-id"]

    def __str__(self):

        return f"{self.student} - {self.lesson} - {self.get_status_display()}"
