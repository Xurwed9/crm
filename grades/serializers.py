from rest_framework import serializers
from accounts.models import User
from lessons.models import Lesson
from students.models import Student
from .models import Grade


class GradeLessonField(serializers.SlugRelatedField):
    def to_representation(self, value):
        return str(value)


class GradeStudentField(serializers.SlugRelatedField):
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
            f"Student with name '{data}' not found. Use 'First Last' format."
        )


class GradeTeacherField(serializers.SlugRelatedField):
    def to_representation(self, value):
        return f"{value.first_name} {value.last_name}".strip() or value.username


class GradeListSerializer(serializers.ModelSerializer):

    lesson = serializers.StringRelatedField()
    student = serializers.StringRelatedField()
    teacher = serializers.StringRelatedField()

    class Meta:
        model = Grade
        fields = (
            "id",
            "lesson",
            "student",
            "teacher",
            "grade",
            "comment",
        )


class GradeDetailSerializer(serializers.ModelSerializer):

    lesson = serializers.StringRelatedField()
    student = serializers.StringRelatedField()
    teacher = serializers.StringRelatedField()

    class Meta:
        model = Grade
        fields = (
            "id",
            "lesson",
            "student",
            "teacher",
            "grade",
            "comment",
            "created_at",
        )


class GradeCreateUpdateSerializer(serializers.ModelSerializer):

    lesson = GradeLessonField(
        slug_field="id",
        queryset=Lesson.objects.all(),
    )
    student = GradeStudentField(
        slug_field="id",
        queryset=Student.objects.all(),
    )
    teacher = GradeTeacherField(
        slug_field="username",
        queryset=User.objects.filter(role="teacher"),
        required=False,
        allow_null=True,
    )

    class Meta:
        model = Grade
        fields = (
            "lesson",
            "student",
            "teacher",
            "grade",
            "comment",
        )
