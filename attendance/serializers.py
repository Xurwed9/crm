from rest_framework import serializers
from .models import Attendance


class AttendanceListSerializer(serializers.ModelSerializer):
    student = serializers.StringRelatedField()
    group = serializers.StringRelatedField()
    teacher = serializers.StringRelatedField()
    status_display = serializers.CharField(
        source="get_status_display",
        read_only=True,
    )
    class Meta:
        model = Attendance
        fields = (
            "id",
            "student",
            "group",
            "teacher",
            "date",
            "status",
            "status_display",
        )


class AttendanceDetailSerializer(serializers.ModelSerializer):


    student = serializers.StringRelatedField()
    group = serializers.StringRelatedField()
    teacher = serializers.StringRelatedField()
    status_display = serializers.CharField(
        source="get_status_display",
        read_only=True,
    )

    class Meta:
        model = Attendance
        fields = (
            "id",
            "student",
            "group",
            "teacher",
            "date",
            "status",
            "status_display",
            "created_at",
            "updated_at",
        )


class AttendanceCreateUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attendance
        fields = (
            "student",
            "group",
            "teacher",
            "date",
            "status",
        )
