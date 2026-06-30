from django.db import models
from lessons.models import Lesson
from accounts.models import User


class JournalComment(models.Model):

    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name="journal_comments",
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="journal_comments",
    )

    content = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.author} - {self.lesson}"
