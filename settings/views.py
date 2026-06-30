from rest_framework.viewsets import ModelViewSet
from accounts.permissions import IsAdmin
from .models import (
    OrganizationSetting, Branch, Room, LessonTime,
    SMTPSetting, TelegramBotSetting, BackupSetting,
)
from .serializers import (
    OrganizationSettingSerializer, BranchSerializer, RoomSerializer,
    LessonTimeSerializer, SMTPSettingSerializer,
    TelegramBotSettingSerializer, BackupSettingSerializer,
)


class OrganizationSettingViewSet(ModelViewSet):
    queryset = OrganizationSetting.objects.all()
    serializer_class = OrganizationSettingSerializer
    permission_classes = [IsAdmin]


class BranchViewSet(ModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    permission_classes = [IsAdmin]


class RoomViewSet(ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAdmin]


class LessonTimeViewSet(ModelViewSet):
    queryset = LessonTime.objects.all()
    serializer_class = LessonTimeSerializer
    permission_classes = [IsAdmin]


class SMTPSettingViewSet(ModelViewSet):
    queryset = SMTPSetting.objects.all()
    serializer_class = SMTPSettingSerializer
    permission_classes = [IsAdmin]


class TelegramBotSettingViewSet(ModelViewSet):
    queryset = TelegramBotSetting.objects.all()
    serializer_class = TelegramBotSettingSerializer
    permission_classes = [IsAdmin]


class BackupSettingViewSet(ModelViewSet):
    queryset = BackupSetting.objects.all()
    serializer_class = BackupSettingSerializer
    permission_classes = [IsAdmin]
