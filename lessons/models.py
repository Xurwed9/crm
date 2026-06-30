from django.db import models
from django.utils.translation import gettext_lazy as _

from accounts.models import User
from groups.models import Group
from courses.models import Course


class Lesson(models.Model):

    LESSON_TYPE_CHOICES = (
        ("normal", _("Normal")),
        ("exam", _("Exam")),
        ("result", _("Result")),
    )

    STATUS_CHOICES = (
        ("planned", _("Planned")),
        ("in_progress", _("In Progress")),
        ("finished", _("Finished")),
    )

    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name="lessons",
        verbose_name=_("Group"),
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="lessons",
        verbose_name=_("Course"),
    )

    teacher = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="lessons",
        limit_choices_to={"role": "teacher"},
        verbose_name=_("Teacher"),
    )

    lesson_number = models.PositiveIntegerField(
        verbose_name=_("Lesson number"),
    )

    lesson_date = models.DateField(
        verbose_name=_("Lesson date"),
    )

    start_time = models.TimeField(
        verbose_name=_("Start time"),
    )

    end_time = models.TimeField(
        verbose_name=_("End time"),
    )

    topic = models.CharField(
        max_length=200,
        verbose_name=_("Topic"),
    )

    description = models.TextField(
        blank=True,
        verbose_name=_("Description"),
    )

    lesson_type = models.CharField(
        max_length=10,
        choices=LESSON_TYPE_CHOICES,
        default="normal",
        verbose_name=_("Lesson type"),
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="planned",
        verbose_name=_("Status"),
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created at"),
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated at"),
    )

    class Meta:
        verbose_name = _("Lesson")
        verbose_name_plural = _("Lessons")
        unique_together = ["group", "lesson_number"]
        ordering = ["lesson_date", "start_time"]

    def __str__(self):
        return f"{self.group} - Lesson {self.lesson_number} - {self.lesson_date}"
