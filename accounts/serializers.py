from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.conf import settings
from django.utils.translation import gettext_lazy as _
import random
from .models import User, Profile


class ProfileSerializer(serializers.ModelSerializer):
    # username = serializers.CharField(source="user.username", read_only=True)
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)
    full_name = serializers.CharField(source="user.get_full_name", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)
    phone_number = serializers.CharField(source="user.phone_number", read_only=True)
    role = serializers.CharField(source="user.role", read_only=True)
    created_at = serializers.DateTimeField(
        source="user.created_at",
        read_only=True,
    )

    class Meta:
        model = Profile
        fields = (
            "id",
            # "username",
            "first_name",
            "last_name",
            "full_name",
            "email",
            "phone_number",
            "role",
            "image",
            "address",
            "bio",
            "birth_date",
            "created_at",
        )
        read_only_fields = fields


class ProfileImageUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            "image",
        )


class UserListSerializer(serializers.ModelSerializer):
    role_display = serializers.CharField(
        source="get_role_display",
        read_only=True,
    )

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "phone_number",
            "role",
            "role_display",
            "is_active",
        )


class UserDetailSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    role_display = serializers.CharField(
        source="get_role_display",
        read_only=True,
    )

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "role",
            "role_display",
            "is_active",
            "created_at",
            "updated_at",
            "profile",
        )
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )


class UserCreateSerializer(serializers.ModelSerializer):
    address = serializers.CharField(required=False, allow_blank=True)
    bio = serializers.CharField(required=False, allow_blank=True)
    birth_date = serializers.DateField(required=False)

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "role",
            "address",
            "bio",
            "birth_date",
        )

    def create(self, validated_data):
        address = validated_data.pop("address", "")
        bio = validated_data.pop("bio", "")
        birth_date = validated_data.pop("birth_date", None)

        raw_password = str(random.randint(10000, 99999))

        user = User.objects.create(
            **validated_data
        )
        user.set_password(raw_password)
        user.save()

        profile = user.profile
        profile.address = address
        profile.bio = bio
        profile.birth_date = birth_date
        profile.save()

        from django.utils import translation
        user_language = getattr(profile, "language", "tg")
        translation.activate(user_language)

        subject = _("CRM Login Information")
        message = _(
            "Hello {first_name} {last_name},\n\n"
            "Your CRM account has been created.\n\n"
            "Login (Phone): {phone_number}\n"
            "Password: {password}\n\n"
        ).format(
            first_name=user.first_name,
            last_name=user.last_name,
            phone_number=user.phone_number,
            password=raw_password,
        )

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )

        translation.deactivate()

        return user


class AdminUserUpdateSerializer(serializers.ModelSerializer):
    address = serializers.CharField(required=False)
    bio = serializers.CharField(required=False)
    birth_date = serializers.DateField(required=False)

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "role",
            "is_active",
            "address",
            "bio",
            "birth_date",
        )

    def update(self, instance, validated_data):
        address = validated_data.pop("address", None)
        bio = validated_data.pop("bio", None)
        birth_date = validated_data.pop("birth_date", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        profile = instance.profile

        if address is not None:
            profile.address = address

        if bio is not None:
            profile.bio = bio

        if birth_date is not None:
            profile.birth_date = birth_date

        profile.save()

        return instance


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(
        label=_("Phone number"),
    )
    password = serializers.CharField(
        write_only=True,
        label=_("Password"),
    )

    def validate(self, attrs):
        user = authenticate(
            phone_number=attrs.get("phone_number"),
            password=attrs.get("password"),
        )
        if user is None:
            raise serializers.ValidationError(
                _("Phone number or password is incorrect.")
            )
        if not user.is_active:
            raise serializers.ValidationError(_("User is inactive."))
        attrs["user"] = user
        return attrs


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(
        write_only=True,
        label=_("Old password"),
    )
    new_password = serializers.CharField(
        write_only=True,
        min_length=8,
        label=_("New password"),
    )

    def validate_old_password(self, value):
        user = self.context.get("request").user
        if not user.check_password(value):
            raise serializers.ValidationError(_("Password is incorrect."))
        return value


class ChangeRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("role",)


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(label=_("Refresh token"))

    def save(self):
        try:
            token = RefreshToken(self.validated_data["refresh"])
            token.blacklist()
        except Exception:
            raise serializers.ValidationError(
                {"detail": _("Invalid or expired refresh token.")}
            )


class ProfileLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ("language",)
