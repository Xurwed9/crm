from django.db import models
from accounts.models import User
from students.models import Student
from lessons.models import Lesson


class Grade(models.Model):

    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name="grades",
    )

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="grades",
    )

    teacher = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="given_grades",
        limit_choices_to={"role": "teacher"},
    )

    grade = models.PositiveSmallIntegerField()

    comment = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        unique_together = ["lesson", "student"]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.student} - {self.lesson} - {self.grade}"
