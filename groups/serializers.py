from rest_framework import serializers
from .models import Group


class GroupListSerializer(serializers.ModelSerializer):
    course = serializers.StringRelatedField()
    teacher = serializers.StringRelatedField()
    status_display = serializers.CharField(
        source="get_status_display",
        read_only=True,
    )

    class Meta:
        model = Group
        fields = (
            "id",
            "name",
            "course",
            "teacher",
            "status",
            "status_display",
        )


class GroupDetailSerializer(serializers.ModelSerializer):
    course = serializers.StringRelatedField()
    teacher = serializers.StringRelatedField()
    students = serializers.StringRelatedField(
        many=True,
        read_only=True,
    )
    status_display = serializers.CharField(
        source="get_status_display",
        read_only=True,
    )

    class Meta:
        model = Group
        fields = (
            "id",
            "name",
            "course",
            "teacher",
            "students",
            "schedule",
            "room",
            "max_students",
            "start_date",
            "end_date",
            "status",
            "status_display",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )


from .models import Group
from courses.models import Course
from teachers.models import Teacher
from students.models import Student

class GroupCreateUpdateSerializer(serializers.ModelSerializer):

    course = serializers.CharField()
    teacher = serializers.CharField()
    students = serializers.ListField(write_only=True)


    class Meta:
        model = Group
        fields = "__all__"


    def create(self, validated_data):

        course_name = validated_data.pop("course")
        teacher_name = validated_data.pop("teacher")
        students_names = validated_data.pop("students")


        course = Course.objects.get(
            name=course_name
        )

        teacher_profile = Teacher.objects.get(
            user__username=teacher_name
        )

        group = Group.objects.create(
            course=course,
            teacher=teacher_profile.user,
            **validated_data
        )


        for name in students_names:
            student = Student.objects.get(
                user__username=name
            )

            group.students.add(student)


        return group