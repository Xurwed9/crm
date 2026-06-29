from rest_framework import serializers
from .models import Lesson


class LessonListSerializer(serializers.ModelSerializer):

    group = serializers.StringRelatedField()
    course = serializers.StringRelatedField()
    teacher = serializers.StringRelatedField()

    lesson_type_display = serializers.CharField(
        source="get_lesson_type_display",
        read_only=True,
    )
    status_display = serializers.CharField(
        source="get_status_display",
        read_only=True,
    )

    class Meta:
        model = Lesson
        fields = (
            "id",
            "group",
            "course",
            "teacher",
            "lesson_number",
            "lesson_date",
            "start_time",
            "end_time",
            "topic",
            "lesson_type",
            "lesson_type_display",
            "status",
            "status_display",
        )


class LessonDetailSerializer(serializers.ModelSerializer):

    group = serializers.StringRelatedField()
    course = serializers.StringRelatedField()
    teacher = serializers.StringRelatedField()
    lesson_type_display = serializers.CharField(
        source="get_lesson_type_display",
        read_only=True,
    )
    status_display = serializers.CharField(
        source="get_status_display",
        read_only=True,
    )

    class Meta:
        model = Lesson
        fields = (
            "id",
            "group",
            "course",
            "teacher",
            "lesson_number",
            "lesson_date",
            "start_time",
            "end_time",
            "topic",
            "description",
            "lesson_type",
            "lesson_type_display",
            "status",
            "status_display",
            "created_at",
            "updated_at",
        )


class LessonCreateUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = (
            "group",
            "course",
            "teacher",
            "lesson_number",
            "lesson_date",
            "start_time",
            "end_time",
            "topic",
            "description",
            "lesson_type",
            "status",
        )


class LessonGenerateSerializer(serializers.Serializer):

    group_id = serializers.IntegerField()
