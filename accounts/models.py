from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("teacher", "Teacher"),
        ("student", "Student"),
    )
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default="student",
    )
    phone_number = models.CharField(
        max_length=20,
        unique=True,
        db_index=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    image = models.ImageField(
        upload_to="profile/",
        blank=True,
        null=True,
    )
    address = models.CharField(
        max_length=200,
        blank=True,
    )
    bio = models.TextField(
        blank=True,
    )
    birth_date = models.DateField(
        blank=True,
        null=True,
    )
    def __str__(self):
        return f"{self.user.username} Profile"