from django.db import models
from accounts.models import User
from students.models import Student
from groups.models import Group
from courses.models import Course


class Grade(models.Model):
    """
    Grade model stores a grade given to a student for a specific lesson.

    Each grade record connects:
      - a student (who received the grade)
      - a teacher (who gave the grade)
      - a group (the class the student belongs to)
      - a course (the subject)
      - a lesson_name (specific topic or lesson title)
      - a grade (numeric score)
      - a comment (optional teacher note)
    """

    # The student who received this grade
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="grades",
    )

    # The teacher who gave this grade (must have teacher role)
    teacher = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="given_grades",
        limit_choices_to={"role": "teacher"},
    )

    # The group/class this grade belongs to
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name="grades",
    )

    # The course/subject this grade is for
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="grades",
    )

    # The specific lesson or topic name
    lesson_name = models.CharField(
        max_length=200,
    )

    # The numeric grade (e.g. 0-100)
    grade = models.PositiveSmallIntegerField()

    # Optional comment from the teacher
    comment = models.TextField(
        blank=True,
    )

    # Automatically set when the record is first created
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    # Automatically updated every time the record is saved
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-created_at", "-id"]

    def __str__(self):
        """
        Returns a readable string like: "John Doe - Math - 85"
        """
        return f"{self.student} - {self.course} - {self.grade}"
