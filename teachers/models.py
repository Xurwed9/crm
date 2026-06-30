from django.db import models
from django.utils.translation import gettext_lazy as _

from accounts.models import User


class Teacher(models.Model):

    STATUS_CHOICES = (
        ("active", _("Active")),
        ("inactive", _("Inactive")),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="teacher",
        verbose_name=_("User"),
    )

    first_name = models.CharField(
        max_length=100,
        verbose_name=_("First name"),
    )

    last_name = models.CharField(
        max_length=100,
        verbose_name=_("Last name"),
    )

    speciality = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("Speciality"),
    )

    address = models.CharField(
        max_length=200,
        blank=True,
        verbose_name=_("Address"),
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="active",
        verbose_name=_("Status"),
    )

    class Meta:
        verbose_name = _("Teacher")
        verbose_name_plural = _("Teachers")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
