from django.db import models
from django.utils.translation import gettext_lazy as _

from students.models import Student
from lessons.models import Lesson


class Attendance(models.Model):

    STATUS_CHOICES = (
        ("present", _("Present")),
        ("absent", _("Absent")),
        ("late", _("Late")),
        ("excused", _("Excused")),
    )

    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name="attendances",
        verbose_name=_("Lesson"),
    )

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="attendances",
        verbose_name=_("Student"),
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="present",
        verbose_name=_("Status"),
    )

    reason = models.TextField(
        blank=True,
        verbose_name=_("Reason"),
    )

    comment = models.TextField(
        blank=True,
        verbose_name=_("Comment"),
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created at"),
    )

    class Meta:
        verbose_name = _("Attendance")
        verbose_name_plural = _("Attendances")
        unique_together = ["lesson", "student"]
        ordering = ["-lesson__lesson_date", "-id"]

    def __str__(self):
        return f"{self.student} - {self.lesson} - {self.get_status_display()}"
