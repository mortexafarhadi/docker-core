from django.contrib.auth.hashers import make_password
from django.db import models

from _0_utils.functions.date_and_time_function import (
    calculate_datetime_breakdown,
)
from _0_utils.functions.generator import uniq_slugify as tc
from _0_utils.functions.password_function import set_salt_password
from _0_utils.models import basic_models as mb
from _0_utils.validator.phone_validator import validate_iranian_phone_number


class RegisterUser(mb.UUIDMixin):
    email = models.EmailField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(
        max_length=10,
        unique=True,
        null=True,
        blank=True,
        validators=[validate_iranian_phone_number],
    )
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    password = models.CharField(max_length=255)
    activation_code = models.CharField(max_length=10)
    send_count = models.PositiveSmallIntegerField(default=0)
    datetime = models.DateTimeField(auto_now_add=True)

    def get_code_token(self):
        return self.activation_code

    def set_activation_code(self):
        self.activation_code = tc.uniq_number_activation_code(self, digits=6)

    def set_password(self, raw_password):
        self.password = make_password(set_salt_password(raw_password))

    def diff_hours(self):
        _diff = calculate_datetime_breakdown(self.datetime)
        return _diff.get("hours", 0)

    def __str__(self):
        res = ""
        if self.email is not None:
            res += self.email
        if self.phone_number is not None:
            res += self.phone_number if res == "" else f" - {self.phone_number}"
        return res if res != "" else self.pk
