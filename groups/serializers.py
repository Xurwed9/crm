from rest_framework import serializers
from .models import Group


class GroupListSerializer(serializers.ModelSerializer):
    course = serializers.StringRelatedField()
    teacher = serializers.SerializerMethodField()
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

    def get_teacher(self, obj):
        if obj.teacher:
            return f"{obj.teacher.first_name} {obj.teacher.last_name}"
        return None


class GroupDetailSerializer(serializers.ModelSerializer):
    course = serializers.StringRelatedField()
    teacher = serializers.SerializerMethodField()
    students = serializers.StringRelatedField(
        many=True,
        read_only=True,
    )

    def get_teacher(self, obj):
        if obj.teacher:
            return f"{obj.teacher.first_name} {obj.teacher.last_name}"
        return None
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


from accounts.models import User
from courses.models import Course
from students.models import Student

class GroupCreateUpdateSerializer(serializers.ModelSerializer):

    course = serializers.CharField()
    teacher = serializers.CharField()
    students = serializers.ListField(write_only=True, required=False, default=list)


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
        )


    def _split_full_name(self, full_name):
        parts = full_name.strip().split(" ", 1)
        if len(parts) < 2:
            raise serializers.ValidationError(
                f"Full name must contain first and last name. Got: '{full_name}'"
            )
        return parts[0], parts[1]

    def validate_course(self, value):
        if not Course.objects.filter(name=value).exists():
            raise serializers.ValidationError(
                f"Course with name '{value}' does not exist."
            )
        return value

    def validate_teacher(self, value):
        first_name, last_name = self._split_full_name(value)
        if not User.objects.filter(
            first_name=first_name,
            last_name=last_name,
            role="teacher",
        ).exists():
            raise serializers.ValidationError(
                f"Teacher with full name '{value}' and role 'teacher' does not exist."
            )
        return value

    def validate(self, data):
        students_names = data.get("students", [])
        for full_name in students_names:
            first_name, last_name = self._split_full_name(full_name)
            if not Student.objects.filter(
                user__first_name=first_name,
                user__last_name=last_name,
            ).exists():
                raise serializers.ValidationError(
                    f"Student with full name '{full_name}' does not exist."
                )
        return data

    def create(self, validated_data):

        course_name = validated_data.pop("course")
        teacher_full_name = validated_data.pop("teacher")
        students_full_names = validated_data.pop("students", [])

        course = Course.objects.get(name=course_name)

        teacher_first, teacher_last = teacher_full_name.split(" ", 1)
        teacher_user = User.objects.get(
            first_name=teacher_first,
            last_name=teacher_last,
            role="teacher",
        )

        group = Group.objects.create(
            course=course,
            teacher=teacher_user,
            **validated_data,
        )

        for full_name in students_full_names:
            s_first, s_last = full_name.split(" ", 1)
            student = Student.objects.get(
                user__first_name=s_first,
                user__last_name=s_last,
            )
            group.students.add(student)

        return group

    def update(self, instance, validated_data):

        course_name = validated_data.pop("course", None)
        teacher_full_name = validated_data.pop("teacher", None)
        students_full_names = validated_data.pop("students", None)

        if course_name:
            instance.course = Course.objects.get(name=course_name)

        if teacher_full_name:
            teacher_first, teacher_last = teacher_full_name.split(" ", 1)
            instance.teacher = User.objects.get(
                first_name=teacher_first,
                last_name=teacher_last,
                role="teacher",
            )

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        if students_full_names is not None:
            instance.students.clear()
            for full_name in students_full_names:
                s_first, s_last = full_name.split(" ", 1)
                student = Student.objects.get(
                    user__first_name=s_first,
                    user__last_name=s_last,
                )
                instance.students.add(student)

        return instance