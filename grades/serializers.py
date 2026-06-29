from rest_framework import serializers
from .models import Grade


class GradeListSerializer(serializers.ModelSerializer):

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
        )


class GradeDetailSerializer(serializers.ModelSerializer):

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
