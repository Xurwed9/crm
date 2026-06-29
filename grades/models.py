from django.db import models
from accounts.models import User
from students.models import Student
from groups.models import Group
from courses.models import Course


class Grade(models.Model):

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

    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name="grades",
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="grades",
    )

    lesson_name = models.CharField(
        max_length=200,
    )

    grade = models.PositiveSmallIntegerField()

    comment = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-created_at", "-id"]

    def __str__(self):

        return f"{self.student} - {self.course} - {self.grade}"
