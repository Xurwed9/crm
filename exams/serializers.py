from rest_framework import serializers
from lessons.models import Lesson
from students.models import Student
from .models import Exam, ExamResult


class ExamLessonField(serializers.SlugRelatedField):
    def to_representation(self, value):
        return str(value)


class ExamStudentField(serializers.SlugRelatedField):
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


class ExamListSerializer(serializers.ModelSerializer):

    lesson = serializers.StringRelatedField()

    class Meta:
        model = Exam
        fields = (
            "id",
            "lesson",
            "title",
            "maximum_score",
            "passing_score",
            "date",
        )


class ExamDetailSerializer(serializers.ModelSerializer):

    lesson = serializers.StringRelatedField()

    class Meta:
        model = Exam
        fields = (
            "id",
            "lesson",
            "title",
            "description",
            "maximum_score",
            "passing_score",
            "date",
            "created_at",
            "updated_at",
        )


class ExamCreateUpdateSerializer(serializers.ModelSerializer):

    lesson = ExamLessonField(
        slug_field="id",
        queryset=Lesson.objects.all(),
    )

    class Meta:
        model = Exam
        fields = (
            "lesson",
            "title",
            "description",
            "maximum_score",
            "passing_score",
            "date",
        )

    def validate_lesson(self, value):
        if value.lesson_type != "exam":
            raise serializers.ValidationError(
                "Exam can only be created for lessons with type 'exam'."
            )
        return value

    def validate(self, data):
        if data.get("passing_score", 0) > data.get("maximum_score", 0):
            raise serializers.ValidationError(
                "Passing score cannot be greater than maximum score."
            )
        return data


class ExamResultListSerializer(serializers.ModelSerializer):

    exam = serializers.StringRelatedField()
    student = serializers.StringRelatedField()

    class Meta:
        model = ExamResult
        fields = (
            "id",
            "exam",
            "student",
            "score",
        )


class ExamResultDetailSerializer(serializers.ModelSerializer):

    exam = serializers.StringRelatedField()
    student = serializers.StringRelatedField()

    class Meta:
        model = ExamResult
        fields = (
            "id",
            "exam",
            "student",
            "score",
            "comment",
            "created_at",
            "updated_at",
        )


class ExamResultCreateUpdateSerializer(serializers.ModelSerializer):

    exam = ExamLessonField(
        slug_field="id",
        queryset=Exam.objects.all(),
    )
    student = ExamStudentField(
        slug_field="id",
        queryset=Student.objects.all(),
    )

    class Meta:
        model = ExamResult
        fields = (
            "exam",
            "student",
            "score",
            "comment",
        )

    def validate(self, data):
        exam = data.get("exam")
        score = data.get("score", 0)

        if score > exam.maximum_score:
            raise serializers.ValidationError(
                f"Score cannot exceed maximum score ({exam.maximum_score})."
            )

        return data
