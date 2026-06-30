from django.db import models
from django.core.exceptions import ValidationError
from students.models import Student
from lessons.models import Lesson


class Exam(models.Model):

    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name="exams",
    )

    title = models.CharField(
        max_length=200,
    )

    description = models.TextField(
        blank=True,
    )

    maximum_score = models.PositiveSmallIntegerField()

    passing_score = models.PositiveSmallIntegerField()

    date = models.DateField()

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-date", "-id"]

    def clean(self):
        if self.lesson.lesson_type != "exam":
            raise ValidationError(
                "Exam can only be created for lessons with type 'exam'."
            )
        if self.passing_score > self.maximum_score:
            raise ValidationError(
                "Passing score cannot be greater than maximum score."
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
    )

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="exam_results",
    )

    score = models.PositiveSmallIntegerField()

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
        unique_together = ["exam", "student"]
        ordering = ["-created_at"]

    def clean(self):
        if self.score > self.exam.maximum_score:
            raise ValidationError(
                f"Score cannot exceed maximum score ({self.exam.maximum_score})."
            )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student} - {self.exam} - {self.score}"
