import re

from django.core.exceptions import ValidationError


def validate_iranian_phone_number(value):
    pattern = r"^9\d{9}$"
    if not value.startswith("9") or len(value) != 10 or not re.match(pattern, value):
        raise ValidationError("Enter a valid phone number")
