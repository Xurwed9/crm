"""
Utility functions for generating lessons from a Group's schedule.

The Group model has a `schedule` field like "Mon Wed Fri 18:00-20:00"
which defines which days of the week and what time the lessons happen.
"""

import re
from datetime import date, timedelta

from .models import Lesson
WEEKDAY_MAP = {
    "mon": 0, "monday": 0,
    "tue": 1, "tuesday": 1,
    "wed": 2, "wednesday": 2,
    "thu": 3, "thursday": 3,
    "fri": 4, "friday": 4,
    "sat": 5, "saturday": 5,
    "sun": 6, "sunday": 6,
}


def parse_schedule(schedule_str):
    time_match = re.search(
        r"(\d{1,2}:\d{2})\s*-\s*(\d{1,2}:\d{2})",
        schedule_str,
    )

    if not time_match:
        return [], None, None

    start_time = time_match.group(1)
    end_time = time_match.group(2)

    days = []
    for word in schedule_str.split():
        clean_word = word.lower().strip(".,;")
        if clean_word in WEEKDAY_MAP:
            days.append(WEEKDAY_MAP[clean_word])

    return sorted(set(days)), start_time, end_time


def generate_lessons_for_group(group):

    days, start_time, end_time = parse_schedule(group.schedule)

    if not days or not start_time or not end_time:
        return 0
    from django.db.models import Max

    existing_max = (
        Lesson.objects.filter(group=group)
        .aggregate(max_num=Max("lesson_number"))
        .get("max_num")
    )
    lesson_number = (existing_max or 0) + 1

    existing_dates = set(
        Lesson.objects.filter(group=group).values_list("lesson_date", flat=True)
    )

    lessons_to_create = []
    current_date = group.start_date

    while current_date <= group.end_date:
        if current_date.weekday() in days:
            if current_date not in existing_dates:
                lessons_to_create.append(
                    Lesson(
                        group=group,
                        course=group.course,
                        teacher=group.teacher,
                        lesson_number=lesson_number,
                        lesson_date=current_date,
                        start_time=start_time,
                        end_time=end_time,
                        topic="",
                        description="",
                        lesson_type="normal",
                        status="planned",
                    )
                )
            lesson_number += 1

        current_date += timedelta(days=1)

    if lessons_to_create:
        Lesson.objects.bulk_create(lessons_to_create)

    return len(lessons_to_create)
