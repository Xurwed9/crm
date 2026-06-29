from django.db import models
from accounts.models import User
from courses.models import Course


class Group(models.Model):

    STATUS_CHOICES = (
        ("active", "Active"),
        ("finished", "Finished"),
        ("closed", "Closed"),
    )

    name = models.CharField(
        max_length=100,
        unique=True,
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="groups",
    )

    teacher = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="teaching_groups",
        limit_choices_to={"role": "teacher"},
    )
    students = models.ManyToManyField(
    "students.Student",
    related_name="groups",
    blank=True
)

    start_date = models.DateField()

    end_date = models.DateField()

    schedule = models.CharField(
        max_length=100,
        help_text="Mon Wed Fri 18:00-20:00",
    )

    room = models.CharField(
        max_length=50,
        blank=True,
    )

    max_students = models.PositiveIntegerField(
        default=20,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="active",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.name