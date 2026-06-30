from rest_framework import serializers
from .models import Exam, ExamResult


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
