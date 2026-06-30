from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from lessons.models import Lesson
from students.models import Student
from .models import Attendance


class LessonSlugField(serializers.SlugRelatedField):
    def to_representation(self, value):
        return str(value)


class StudentSlugField(serializers.SlugRelatedField):
    def to_representation(self, value):
        return str(value)

    def to_internal_value(self, data):
        if isinstance(data, int):
            return Student.objects.get(pk=data)
        parts = data.strip().split(" ", 1)
        if len(parts) == 2:
            first, last = parts
            try:
                return Student.objects.get(first_name=first, last_name=last)
            except Student.DoesNotExist:
                pass
        try:
            return Student.objects.get(user__username=data)
        except Student.DoesNotExist:
            pass
        raise serializers.ValidationError(
            _("Student with name '{}' not found. Use 'First Last' format.").format(data)
        )


class AttendanceListSerializer(serializers.ModelSerializer):

    lesson = serializers.StringRelatedField()
    student = serializers.StringRelatedField()
    status_display = serializers.CharField(
        source="get_status_display",
        read_only=True,
    )

    class Meta:
        model = Attendance
        fields = (
            "id",
            "lesson",
            "student",
            "status",
            "status_display",
        )


class AttendanceDetailSerializer(serializers.ModelSerializer):

    lesson = serializers.StringRelatedField()
    student = serializers.StringRelatedField()
    status_display = serializers.CharField(
        source="get_status_display",
        read_only=True,
    )

    class Meta:
        model = Attendance
        fields = (
            "id",
            "lesson",
            "student",
            "status",
            "status_display",
            "reason",
            "comment",
            "created_at",
        )


class AttendanceCreateUpdateSerializer(serializers.ModelSerializer):

    lesson = LessonSlugField(
        slug_field="id",
        queryset=Lesson.objects.all(),
    )
    student = StudentSlugField(
        slug_field="id",
        queryset=Student.objects.all(),
    )

    class Meta:
        model = Attendance
        fields = (
            "lesson",
            "student",
            "status",
            "reason",
            "comment",
        )
