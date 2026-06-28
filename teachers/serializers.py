import random

from rest_framework import serializers
from django.core.mail import send_mail

from accounts.models import User
from .models import Teacher


def generate_password():
    return str(random.randint(10000, 99999))


class TeacherSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(write_only=True)
    username = serializers.CharField(write_only=True)
    phone_number = serializers.CharField(write_only=True)


    class Meta:
        model = Teacher
        fields = [
            "id",
            "username",
            "email",
            "phone_number",
            "first_name",
            "last_name",
            "speciality",
            "address",
            "status",
        ]


    def create(self, validated_data):

        email = validated_data.pop("email")
        username = validated_data.pop("username")
        phone = validated_data.pop("phone_number")


        first_name = validated_data.get("first_name")
        last_name = validated_data.get("last_name")


        password = generate_password()

        print("TEACHER PASSWORD:", password)
        user = User.objects.create_user(
            username=username,
            email=email,
            phone_number=phone,
            password=password,
            role="teacher",
            first_name=first_name,
            last_name=last_name,
        )


        send_mail(
            "CRM Teacher Login",
            f"""
Your CRM account:

Phone: {phone}
Password: {password}
""",
            "your_email@gmail.com",
            [email],
        )
        print(password)


        teacher = Teacher.objects.create(
            user=user,
            **validated_data
        )


        return teacher