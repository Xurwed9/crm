from django.db import models
from accounts.models import User
from groups.models import Group
from courses.models import Course


class Lesson(models.Model):

    LESSON_TYPE_CHOICES = (
        ("normal", "Normal"),
        ("exam", "Exam"),
        ("result", "Result"),
    )

    STATUS_CHOICES = (
        ("planned", "Planned"),
        ("in_progress", "In Progress"),
        ("finished", "Finished"),
    )

    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name="lessons",
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="lessons",
    )

    teacher = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="lessons",
        limit_choices_to={"role": "teacher"},
    )

    lesson_number = models.PositiveIntegerField()

    lesson_date = models.DateField()

    start_time = models.TimeField()

    end_time = models.TimeField()

    topic = models.CharField(
        max_length=200,
    )

    description = models.TextField(
        blank=True,
    )

    lesson_type = models.CharField(
        max_length=10,
        choices=LESSON_TYPE_CHOICES,
        default="normal",
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="planned",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        unique_together = ["group", "lesson_number"]
        ordering = ["lesson_date", "start_time"]

    def __str__(self):

        return f"{self.group} - Lesson {self.lesson_number} - {self.lesson_date}"
