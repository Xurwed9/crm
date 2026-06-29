from rest_framework import serializers
from .models import Grade


class GradeListSerializer(serializers.ModelSerializer):
    """
    Used when returning a list of grade records.

    Shows related objects (student, teacher, group, course) as readable
    strings instead of raw IDs.
    """

    # Display the student's full name
    student = serializers.StringRelatedField()

    # Display the teacher's username
    teacher = serializers.StringRelatedField()

    # Display the group's name
    group = serializers.StringRelatedField()

    # Display the course name
    course = serializers.StringRelatedField()

    class Meta:
        model = Grade
        fields = (
            "id",
            "student",
            "teacher",
            "group",
            "course",
            "lesson_name",
            "grade",
            "comment",
        )


class GradeDetailSerializer(serializers.ModelSerializer):
    """
    Used when viewing a single grade record in detail.

    Includes all fields from the list serializer plus timestamps.
    """

    student = serializers.StringRelatedField()
    teacher = serializers.StringRelatedField()
    group = serializers.StringRelatedField()
    course = serializers.StringRelatedField()

    class Meta:
        model = Grade
        fields = (
            "id",
            "student",
            "teacher",
            "group",
            "course",
            "lesson_name",
            "grade",
            "comment",
            "created_at",
            "updated_at",
        )


class GradeCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Used when creating or updating a grade record.

    Accepts foreign keys as integer IDs (student ID, teacher ID, group ID,
    course ID) along with the lesson name, grade, and optional comment.
    """

    class Meta:
        model = Grade
        fields = (
            "student",
            "teacher",
            "group",
            "course",
            "lesson_name",
            "grade",
            "comment",
        )
