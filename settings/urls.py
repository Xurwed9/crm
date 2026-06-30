from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    OrganizationSettingViewSet, BranchViewSet, RoomViewSet,
    LessonTimeViewSet, SMTPSettingViewSet,
    TelegramBotSettingViewSet, BackupSettingViewSet,
)

router = DefaultRouter()
router.register("organization", OrganizationSettingViewSet)
router.register("branches", BranchViewSet)
router.register("rooms", RoomViewSet)
router.register("lesson-times", LessonTimeViewSet)
router.register("smtp", SMTPSettingViewSet)
router.register("telegram-bot", TelegramBotSettingViewSet)
router.register("backups", BackupSettingViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
