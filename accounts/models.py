from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    ROLE_CHOICES = (
        ("admin", _("Admin")),
        ("teacher", _("Teacher")),
        ("student", _("Student")),
    )
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default="student",
        verbose_name=_("Role"),
    )
    phone_number = models.CharField(
        max_length=20,
        unique=True,
        db_index=True,
        verbose_name=_("Phone number"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created at"),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated at"),
    )
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


class Profile(models.Model):
    LANGUAGE_CHOICES = (
        ("tg", _("Tajik")),
        ("ru", _("Russian")),
        ("en", _("English")),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name=_("User"),
    )
    image = models.ImageField(
        upload_to="profile/",
        blank=True,
        null=True,
        verbose_name=_("Image"),
    )
    address = models.CharField(
        max_length=200,
        blank=True,
        verbose_name=_("Address"),
    )
    bio = models.TextField(
        blank=True,
        verbose_name=_("Biography"),
    )
    birth_date = models.DateField(
        blank=True,
        null=True,
        verbose_name=_("Birth date"),
    )
    language = models.CharField(
        max_length=2,
        choices=LANGUAGE_CHOICES,
        default="tg",
        verbose_name=_("Language"),
    )

    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")

    def __str__(self):
        return f"{self.user.username} Profile"