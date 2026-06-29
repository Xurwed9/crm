from django.db import models
from students.models import Student
from lessons.models import Lesson


class Attendance(models.Model):
    """
    Attendance records which student attended which lesson and their status.

    Ties a student to a specific lesson with a status of:
      Present, Absent, Late, or Excused.

    Only one attendance record per student per lesson is allowed.
    """

    # The four possible attendance statuses
    STATUS_CHOICES = (
        ("present", "Present"),
        ("absent", "Absent"),
        ("late", "Late"),
        ("excused", "Excused"),
    )

    # Which lesson this attendance record is for
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name="attendances",
    )

    # Which student this attendance record is about
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="attendances",
    )

    # Attendance status: Present, Absent, Late, or Excused
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="present",
    )

    # Reason for absence/lateness (optional)
    reason = models.TextField(
        blank=True,
    )

    # Additional teacher comment (optional)
    comment = models.TextField(
        blank=True,
    )

    # Automatically set when the record is first created
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        # Prevents duplicate attendance for the same student in the same lesson
        unique_together = ["lesson", "student"]
        ordering = ["-lesson__lesson_date", "-id"]

    def __str__(self):
        """
        Returns a readable string like:
        "John Doe - Lesson 5 - Present"
        """
        return f"{self.student} - {self.lesson} - {self.get_status_display()}"
