import random

from rest_framework import serializers
from django.core.mail import send_mail
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from accounts.models import User
from .models import Teacher


def generate_password():
    return str(random.randint(10000, 99999))


class TeacherSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(
        write_only=True,
        label=_("Email"),
    )
    username = serializers.CharField(
        write_only=True,
        label=_("Username"),
    )
    phone_number = serializers.CharField(
        write_only=True,
        label=_("Phone number"),
    )

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

        user = User.objects.create_user(
            username=username,
            email=email,
            phone_number=phone,
            password=password,
            role="teacher",
            first_name=first_name,
            last_name=last_name,
        )

        from django.utils import translation
        user_language = getattr(user.profile, "language", "tg")
        translation.activate(user_language)

        subject = _("CRM Teacher Login")
        message = _(
            "Your CRM account:\n\n"
            "Phone: {phone}\n"
            "Password: {password}\n"
        ).format(phone=phone, password=password)

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [email],
        )

        translation.deactivate()

        teacher = Teacher.objects.create(
            user=user,
            **validated_data
        )

        return teacher
