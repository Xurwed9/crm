from rest_framework import serializers
from .models import Attendance


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

    class Meta:
        model = Attendance
        fields = (
            "lesson",
            "student",
            "status",
            "reason",
            "comment",
        )
