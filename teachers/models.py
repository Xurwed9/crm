from django.db import models
from accounts.models import User


class Teacher(models.Model):

    STATUS_CHOICES = (
        ("active", "Active"),
        ("inactive", "Inactive"),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="teacher"
    )

    first_name = models.CharField(
        max_length=100
    )

    last_name = models.CharField(
        max_length=100
    )

    speciality = models.CharField(
        max_length=100,
        blank=True
    )

    address = models.CharField(
        max_length=200,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="active"
    )


    def __str__(self):
        return f"{self.first_name} {self.last_name}"