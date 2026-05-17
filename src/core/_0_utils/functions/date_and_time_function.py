import datetime

import pytz
from django.conf import settings
from django.utils import timezone as tz
from jalali_date import date2jalali

JALALI_MONTHS_FA = {
    1: "فروردین",
    2: "اردیبهشت",
    3: "خرداد",
    4: "تیر",
    5: "مرداد",
    6: "شهریور",
    7: "مهر",
    8: "آبان",
    9: "آذر",
    10: "دی",
    11: "بهمن",
    12: "اسفند",
}


def now():
    return tz.now().astimezone(pytz.timezone(settings.TIME_ZONE))


def generate_timedelta_days(value):
    return datetime.timedelta(days=value)


def generate_timedelta_minutes(value):
    return datetime.timedelta(minutes=value)


def generate_timedelta_seconds(value):
    return datetime.timedelta(seconds=value)


def datetime_str_to_obj__datetime(datetime_str):
    return datetime.datetime.fromisoformat(datetime_str)


def datetime_obj_to_str__datetime(datetime_obj, style="-"):
    return datetime.datetime.strftime(datetime_obj, f"%Y{style}%m{style}%d %H:%M:%S")


def date_str_to_obj__datetime(date_str, format_="%Y/%m/%d"):
    return tz.make_aware(
        datetime.datetime.strptime(date_str, format_),
        timezone=pytz.timezone(settings.TIME_ZONE),
    )


def datetime_obj_to_str__date(datetime_obj, style="-"):
    return datetime_obj_to_str__datetime(datetime_obj, style).split(" ")[0]


def date_obj_to_str__date(date_obj, style="-"):
    return datetime.date.strftime(date_obj, f"%Y{style}%m{style}%d")


def to_timestamp(date_str, style="/"):
    return datetime.datetime.strptime(date_str, f"%Y{style}%m{style}%d").timestamp()


def seconds_to_years(seconds_with_ms):
    """Converts seconds (with milliseconds as decimal) to years."""
    total_seconds = seconds_with_ms
    seconds_in_year = 31536000  # Approximate number of seconds in a year
    return total_seconds / seconds_in_year


def seconds_to_months(seconds_with_ms):
    """Converts seconds (with milliseconds as decimal) to months."""
    total_seconds = seconds_with_ms
    seconds_in_month = 2592000  # Average seconds in a month (30 days average)
    return total_seconds / seconds_in_month


def seconds_to_weeks(seconds_with_ms):
    """Converts seconds (with milliseconds as decimal) to weeks."""
    total_seconds = seconds_with_ms
    seconds_in_week = 604800
    return total_seconds / seconds_in_week


def seconds_to_days(seconds_with_ms):
    """Converts seconds (with milliseconds as decimal) to days."""
    total_seconds = seconds_with_ms
    seconds_in_day = 86400
    return total_seconds / seconds_in_day


def seconds_to_hours(seconds_with_ms):
    """Converts seconds (with milliseconds as decimal) to hours."""
    total_seconds = seconds_with_ms
    seconds_in_hour = 3600
    return total_seconds / seconds_in_hour


def seconds_to_minutes(seconds_with_ms):
    """Converts seconds (with milliseconds as decimal) to minutes."""
    total_seconds = seconds_with_ms
    seconds_in_minute = 60
    return total_seconds / seconds_in_minute


def calculate_diff_time(datetime_obj):
    _now = now()
    if not tz.is_aware(datetime_obj):
        datetime_obj = tz.make_aware(datetime_obj, _now.tzinfo)
    diff_time = _now - datetime_obj
    total_seconds = diff_time.total_seconds()
    return diff_time, total_seconds


def calculate_datetime_breakdown(datetime_str):
    diff_time, total_seconds = calculate_diff_time(datetime_str)
    days = diff_time.days
    years = days // 365
    months = (days % 365) // 30
    days = days % 30
    hours, remainder = divmod(diff_time.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    result = {
        "years": years,
        "months": months,
        "days": days,
        "hours": hours,
        "minutes": minutes,
        "seconds": seconds
    }
    return result


def calculate_years_breakdown(datetime_str):
    diff_time, total_seconds = calculate_diff_time(datetime_str)
    days = diff_time.days
    years = days // 365
    return years


def calculate_months_breakdown(datetime_str):
    diff_time, total_seconds = calculate_diff_time(datetime_str)
    days = diff_time.days
    months = days // 30
    return months


def calculate_weeks_breakdown(datetime_str):
    diff_time, total_seconds = calculate_diff_time(datetime_str)
    days = diff_time.days
    months = days // 7
    return months


def generate_time_slots(start_time, end_time, duration_minutes=30):
    slots = []
    current = datetime.datetime.combine(datetime.datetime.today(), start_time)
    end = datetime.datetime.combine(datetime.datetime.today(), end_time)

    while current + generate_timedelta_minutes(duration_minutes) <= end:
        slots.append(current.time())
        current += generate_timedelta_minutes(duration_minutes)
    return slots


def generate_weekday_date():
    today = datetime.date.today()
    start_of_week = today - generate_timedelta_days(today.weekday())
    days_of_week = [
        "monday",
        "tuesday",
        "wednesday",
        "thursday",
        "friday",
        "saturday",
        "sunday",
    ]

    result = {}
    for i in range(7):
        i -= 2
        day_date = start_of_week + generate_timedelta_days(i)
        day_index = day_date.weekday()
        day_name = days_of_week[day_index]
        result[day_name] = day_date
    return result


def generate_current_next_week_weekday_date():
    today = datetime.date.today()
    start_of_week = today - generate_timedelta_days(today.weekday())
    start_of_next_week = start_of_week + generate_timedelta_days(7)
    days_of_week = [
        "monday",
        "tuesday",
        "wednesday",
        "thursday",
        "friday",
        "saturday",
        "sunday",
    ]

    result = {"current_week": {}, "next_week": {}}
    for i in range(7):
        i -= 2
        day_date_current = start_of_week + generate_timedelta_days(i)
        day_date_next = start_of_next_week + generate_timedelta_days(i)
        day_index = day_date_current.weekday()
        day_name = days_of_week[day_index]
        result["current_week"][day_name] = day_date_current
        result["next_week"][day_name] = day_date_next
    return result


def duration_to_time(duration):
    total_seconds = duration.total_seconds()
    hours = int(total_seconds // 3600)
    remaining_seconds = int(total_seconds % 3600)
    minutes = int(remaining_seconds // 60)
    seconds = int(remaining_seconds % 60)
    return datetime.time(hour=hours, minute=minutes, second=seconds)


def second_to_duration__str(total_seconds: int) -> str:
    """Format seconds into Y M D H M S (only non-zero units)."""

    seconds = int(total_seconds)

    year = seconds // (365 * 24 * 3600)
    seconds %= 365 * 24 * 3600

    month = seconds // (30 * 24 * 3600)
    seconds %= 30 * 24 * 3600

    day = seconds // (24 * 3600)
    seconds %= 24 * 3600

    hour = seconds // 3600
    seconds %= 3600

    minute = seconds // 60
    seconds %= 60

    # Only show units that are > 0
    parts = []
    if year > 0:
        parts.append(f"{year}y")
    if month > 0:
        parts.append(f"{month}mo")
    if day > 0:
        parts.append(f"{day}d")
    if hour > 0:
        parts.append(f"{hour}h")
    if minute > 0:
        parts.append(f"{minute}m")
    if seconds > 0:
        parts.append(f"{seconds}s")

    # If everything is zero, return "0s"
    return " ".join(parts) if parts else "0s"


def convert_datetime_to_jalali(value):
    return date2jalali(value)


def datetime_to_jalali_date__full_date__str_month(value):
    j = convert_datetime_to_jalali(value)
    return f"{j.year} {JALALI_MONTHS_FA[j.month]} {j.day}"


def datetime_to_jalali_date__month_day__str_month(value):
    j = convert_datetime_to_jalali(value)
    return f"{j.day} {JALALI_MONTHS_FA[j.month]}"


def time_remove_seconds__str(value):
    return str(value)[:-3]
