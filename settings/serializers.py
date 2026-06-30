from rest_framework import serializers
from .models import (
    OrganizationSetting, Branch, Room, LessonTime,
    SMTPSetting, TelegramBotSetting, BackupSetting,
)


class OrganizationSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationSetting
        fields = "__all__"


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = "__all__"


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"


class LessonTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonTime
        fields = "__all__"


class SMTPSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SMTPSetting
        fields = "__all__"


class TelegramBotSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramBotSetting
        fields = "__all__"


class BackupSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = BackupSetting
        fields = "__all__"
