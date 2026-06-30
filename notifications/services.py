import json
import logging
from urllib import request as urllib_request
from urllib.error import URLError

from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger(__name__)


EVENT_TEMPLATES = {
    "user_created": {
        "subject": _("Welcome to CRM System"),
        "body": _(
            "Hello {first_name} {last_name},\n\n"
            "Your account has been created successfully.\n\n"
            "Username: {username}\n"
            "Role: {role}\n"
            "Phone: {phone_number}"
        ),
    },
    "homework_assigned": {
        "subject": _("New Homework: {title}"),
        "body": _(
            "Hello {first_name},\n\n"
            "New homework has been assigned.\n\n"
            "Lesson: {lesson_topic}\n"
            "Homework: {title}\n"
            "Deadline: {deadline}\n\n"
            "{description}"
        ),
    },
    "exam_scheduled": {
        "subject": _("Exam Scheduled: {title}"),
        "body": _(
            "Hello {first_name},\n\n"
            "An exam has been scheduled.\n\n"
            "Lesson: {lesson_topic}\n"
            "Exam: {title}\n"
            "Date: {date}\n"
            "Maximum Score: {maximum_score}\n"
            "Passing Score: {passing_score}"
        ),
    },
    "payment_reminder": {
        "subject": _("Payment Reminder"),
        "body": _(
            "Hello {first_name},\n\n"
            "This is a reminder about your pending payment.\n\n"
            "Amount: {amount}\n"
            "Due Date: {due_date}\n\n"
            "Please make the payment at your earliest convenience."
        ),
    },
    "absent": {
        "subject": _("Absence Notification"),
        "body": _(
            "Hello {first_name},\n\n"
            "You were marked absent for the following lesson:\n\n"
            "Date: {lesson_date}\n"
            "Lesson: {lesson_topic}\n"
            "Group: {group_name}\n\n"
            "Please contact your teacher for more information."
        ),
    },
    "custom": {
        "subject": _("{subject}"),
        "body": _("{message}"),
    },
}


def build_message(event_type, extra_data):
    template = EVENT_TEMPLATES.get(event_type)
    if not template:
        return None, None

    safe = {}
    if extra_data:
        for k, v in extra_data.items():
            safe[k] = str(v) if v is not None else ""

    try:
        subject = template["subject"].format(**safe)
        body = template["body"].format(**safe)
    except KeyError as e:
        subject = template["subject"]
        body = template["body"]
        logger.warning(f"Missing template variable for {event_type}: {e}")

    return subject, body


class EmailService:

    @staticmethod
    def send(recipient_email, subject, body):

        if not recipient_email:
            return False, "No email address"

        try:
            send_mail(
                subject,
                body,
                settings.DEFAULT_FROM_EMAIL,
                [recipient_email],
                fail_silently=False,
            )
            return True, None
        except Exception as e:
            logger.error(f"Email send failed to {recipient_email}: {e}")
            return False, str(e)


class SMSService:

    @staticmethod
    def send(phone_number, message):

        if not phone_number:
            return False, "No phone number"

        try:
            logger.info(f"SMS to {phone_number}: {message}")
            return True, None
        except Exception as e:
            logger.error(f"SMS send failed to {phone_number}: {e}")
            return False, str(e)


class TelegramService:

    @staticmethod
    def send(chat_id, message):

        if not chat_id:
            return False, "No Telegram chat ID"

        bot_token = getattr(settings, "TELEGRAM_BOT_TOKEN", None)
        if not bot_token:
            return False, "TELEGRAM_BOT_TOKEN not configured"

        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = json.dumps({
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "HTML",
        }).encode()

        req = urllib_request.Request(
            url, data=payload, headers={"Content-Type": "application/json"},
        )

        try:
            urllib_request.urlopen(req, timeout=10)
            return True, None
        except URLError as e:
            logger.error(f"Telegram send failed to chat {chat_id}: {e}")
            return False, str(e)


SERVICE_MAP = {
    "email": EmailService,
    "sms": SMSService,
    "telegram": TelegramService,
}


def send_notification(recipient, event_type, channels, extra_data=None):

    subject, body = build_message(event_type, extra_data)
    if not subject:
        return []

    results = []
    for channel in channels:
        service_cls = SERVICE_MAP.get(channel)
        if not service_cls:
            continue

        if channel == "email":
            success, error = service_cls.send(recipient.email, subject, body)
        elif channel == "sms":
            success, error = service_cls.send(recipient.phone_number, body)
        elif channel == "telegram":
            chat_id = getattr(
                getattr(recipient, "notification_settings", None),
                "telegram_chat_id",
                None,
            )
            success, error = service_cls.send(chat_id, body)
        else:
            success, error = False, "Unknown channel"

        from .models import NotificationLog

        NotificationLog.objects.create(
            event_type=event_type,
            channel=channel,
            recipient=recipient,
            subject=subject,
            body=body,
            status="sent" if success else "failed",
            sent_at=timezone.now() if success else None,
            error_message=error if not success else "",
        )

        results.append({"channel": channel, "success": success, "error": error})

    return results
