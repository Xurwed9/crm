from django.db import models
from django.utils.translation import gettext_lazy as _

from accounts.models import User
from courses.models import Course


class Group(models.Model):

    STATUS_CHOICES = (
        ("active", _("Active")),
        ("finished", _("Finished")),
        ("closed", _("Closed")),
    )

    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_("Name"),
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="groups",
        verbose_name=_("Course"),
    )

    teacher = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="teaching_groups",
        limit_choices_to={"role": "teacher"},
        verbose_name=_("Teacher"),
    )
    students = models.ManyToManyField(
        "students.Student",
        related_name="groups",
        blank=True,
        verbose_name=_("Students"),
    )

    start_date = models.DateField(
        verbose_name=_("Start date"),
    )

    end_date = models.DateField(
        verbose_name=_("End date"),
    )

    schedule = models.CharField(
        max_length=100,
        help_text=_("Mon Wed Fri 18:00-20:00"),
        verbose_name=_("Schedule"),
    )

    room = models.CharField(
        max_length=50,
        blank=True,
        verbose_name=_("Room"),
    )

    max_students = models.PositiveIntegerField(
        default=20,
        verbose_name=_("Maximum students"),
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="active",
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
        verbose_name = _("Group")
        verbose_name_plural = _("Groups")
        ordering = ["-id"]

    def __str__(self):
        return self.name
