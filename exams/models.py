from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from students.models import Student
from lessons.models import Lesson


class Exam(models.Model):

    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name="exams",
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

    maximum_score = models.PositiveSmallIntegerField(
        verbose_name=_("Maximum score"),
    )

    passing_score = models.PositiveSmallIntegerField(
        verbose_name=_("Passing score"),
    )

    date = models.DateField(
        verbose_name=_("Date"),
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
        verbose_name = _("Exam")
        verbose_name_plural = _("Exams")
        ordering = ["-date", "-id"]

    def clean(self):
        if self.lesson.lesson_type != "exam":
            raise ValidationError(
                _("Exam can only be created for lessons with type 'exam'.")
            )
        if self.passing_score > self.maximum_score:
            raise ValidationError(
                _("Passing score cannot be greater than maximum score.")
            )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} - {self.lesson}"


class ExamResult(models.Model):

    exam = models.ForeignKey(
        Exam,
        on_delete=models.CASCADE,
        related_name="results",
        verbose_name=_("Exam"),
    )

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="exam_results",
        verbose_name=_("Student"),
    )

    score = models.PositiveSmallIntegerField(
        verbose_name=_("Score"),
    )

    comment = models.TextField(
        blank=True,
        verbose_name=_("Comment"),
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
        verbose_name = _("Exam result")
        verbose_name_plural = _("Exam results")
        unique_together = ["exam", "student"]
        ordering = ["-created_at"]

    def clean(self):
        if self.score > self.exam.maximum_score:
            raise ValidationError(
                _("Score cannot exceed maximum score ({max_score}).").format(max_score=self.exam.maximum_score)
            )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student} - {self.exam} - {self.score}"
