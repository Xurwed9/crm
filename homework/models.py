from django.db import models
from django.utils.translation import gettext_lazy as _

from accounts.models import User
from students.models import Student
from lessons.models import Lesson


class Homework(models.Model):

    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name="homeworks",
        verbose_name=_("Lesson"),
    )

    title = models.CharField(
        max_length=200,
        verbose_name=_("Title"),
    )

    description = models.TextField(
        blank=True,
        verbose_name=_("Description"),
    )

    deadline = models.DateTimeField(
        verbose_name=_("Deadline"),
    )

    attachment = models.FileField(
        upload_to="homeworks/attachments/",
        blank=True,
        null=True,
        verbose_name=_("Attachment"),
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created at"),
    )

    class Meta:
        verbose_name = _("Homework")
        verbose_name_plural = _("Homeworks")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.lesson} - {self.title}"


class Submission(models.Model):

    homework = models.ForeignKey(
        Homework,
        on_delete=models.CASCADE,
        related_name="submissions",
        verbose_name=_("Homework"),
    )

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="submissions",
        verbose_name=_("Student"),
    )

    answer = models.FileField(
        upload_to="homeworks/answers/",
        blank=True,
        null=True,
        verbose_name=_("Answer"),
    )

    grade = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        verbose_name=_("Grade"),
    )

    feedback = models.TextField(
        blank=True,
        verbose_name=_("Feedback"),
    )

    submitted_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Submitted at"),
    )

    graded_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Graded at"),
    )

    class Meta:
        verbose_name = _("Submission")
        verbose_name_plural = _("Submissions")
        unique_together = ["homework", "student"]
        ordering = ["-submitted_at"]

    def __str__(self):
        return f"{self.student} - {self.homework.title}"
