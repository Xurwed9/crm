import random

from rest_framework import serializers
from django.core.mail import send_mail
from django.conf import settings

from accounts.models import User
from .models import Student


def generate_password():
    return str(random.randint(10000, 99999))


class StudentSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(write_only=True)
    username = serializers.CharField(write_only=True)
    phone_number = serializers.CharField(write_only=True)

    class Meta:
        model = Student
        fields = [
            "id",
            "username",
            "email",
            "phone_number",
            "first_name",
            "last_name",
            "birth_date",
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

        user = User.objects.create_user(
    username=username,
    email=email,
    phone_number=phone,
    password=password,
    role="student",
    first_name=validated_data.get("first_name"),
    last_name=validated_data.get("last_name"),
)


        send_mail(
            "CRM Login",
            f"""
Your CRM account:

Phone: {phone}
Password: {password}
""",
            settings.DEFAULT_FROM_EMAIL,
            [email],
        )


        student = Student.objects.create(
            user=user,
            **validated_data
        )

        return student