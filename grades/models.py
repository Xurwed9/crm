from django.db import models
from django.utils.translation import gettext_lazy as _

from accounts.models import User
from students.models import Student
from lessons.models import Lesson


class Grade(models.Model):

    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name="grades",
        verbose_name=_("Lesson"),
    )

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="grades",
        verbose_name=_("Student"),
    )

    teacher = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="given_grades",
        limit_choices_to={"role": "teacher"},
        verbose_name=_("Teacher"),
    )

    grade = models.PositiveSmallIntegerField(
        verbose_name=_("Grade"),
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
        verbose_name = _("Grade")
        verbose_name_plural = _("Grades")
        unique_together = ["lesson", "student"]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.student} - {self.lesson} - {self.grade}"
