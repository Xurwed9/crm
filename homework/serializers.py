from rest_framework import serializers
from lessons.models import Lesson
from .models import Homework, Submission


class HomeworkLessonField(serializers.SlugRelatedField):
    def to_representation(self, value):
        return str(value)


class HomeworkListSerializer(serializers.ModelSerializer):


    lesson = serializers.StringRelatedField()

    class Meta:
        model = Homework
        fields = (
            "id",
            "lesson",
            "title",
            "deadline",
            "created_at",
        )


class HomeworkDetailSerializer(serializers.ModelSerializer):


    lesson = serializers.StringRelatedField()

    class Meta:
        model = Homework
        fields = (
            "id",
            "lesson",
            "title",
            "description",
            "deadline",
            "attachment",
            "created_at",
        )


class HomeworkCreateUpdateSerializer(serializers.ModelSerializer):

    lesson = HomeworkLessonField(
        slug_field="id",
        queryset=Lesson.objects.all(),
    )

    class Meta:
        model = Homework
        fields = (
            "lesson",
            "title",
            "description",
            "deadline",
            "attachment",
        )


class SubmissionListSerializer(serializers.ModelSerializer):

    homework = serializers.StringRelatedField()
    student = serializers.StringRelatedField()

    class Meta:
        model = Submission
        fields = (
            "id",
            "homework",
            "student",
            "grade",
            "submitted_at",
            "graded_at",
        )


class SubmissionDetailSerializer(serializers.ModelSerializer):


    homework = serializers.StringRelatedField()
    student = serializers.StringRelatedField()

    class Meta:
        model = Submission
        fields = (
            "id",
            "homework",
            "student",
            "answer",
            "grade",
            "feedback",
            "submitted_at",
            "graded_at",
        )


class SubmissionCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Submission
        fields = (
            "homework",
            "answer",
        )


class SubmissionGradeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Submission
        fields = (
            "grade",
            "feedback",
        )
