from rest_framework import serializers
from .models import Grade


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


    class Meta:
        model = Grade
        fields = (
            "lesson",
            "student",
            "teacher",
            "grade",
            "comment",
        )
