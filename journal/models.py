from django.db import models
from django.utils.translation import gettext_lazy as _

from lessons.models import Lesson
from accounts.models import User


class JournalComment(models.Model):

    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name="journal_comments",
        verbose_name=_("Lesson"),
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="journal_comments",
        verbose_name=_("Author"),
    )

    content = models.TextField(
        verbose_name=_("Content"),
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
        verbose_name = _("Journal comment")
        verbose_name_plural = _("Journal comments")
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.author} - {self.lesson}"
