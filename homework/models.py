from django.db import models
from accounts.models import User
from students.models import Student
from lessons.models import Lesson


class Homework(models.Model):

    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name="homeworks",
    )

    title = models.CharField(
        max_length=200,
    )

    description = models.TextField(
        blank=True,
    )

    deadline = models.DateTimeField()

    attachment = models.FileField(
        upload_to="homeworks/attachments/",
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.lesson} - {self.title}"


class Submission(models.Model):

    homework = models.ForeignKey(
        Homework,
        on_delete=models.CASCADE,
        related_name="submissions",
    )

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="submissions",
    )

    answer = models.FileField(
        upload_to="homeworks/answers/",
        blank=True,
        null=True,
    )

    grade = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
    )

    feedback = models.TextField(
        blank=True,
    )

    submitted_at = models.DateTimeField(
        auto_now_add=True,
    )

    graded_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    class Meta:
        unique_together = ["homework", "student"]
        ordering = ["-submitted_at"]

    def __str__(self):
        return f"{self.student} - {self.homework.title}"
