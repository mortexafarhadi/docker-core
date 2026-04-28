from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

from ___utils.functions.generator import uniq_slugify as tc
from ___utils.functions.generator.url_image_base import get_image_thumbnail
from ___utils.functions.password_function import set_salt_password
from ___utils.models import basic_models as mb


class User(AbstractUser, mb.BasicCKEditorModelHistorical):
    class GENDER_CHOICES(models.TextChoices):
        NOT_SELECTED = (
            "not_selected",
            "Not Selected",
        )
        MALE = (
            "male",
            "Male",
        )
        FEMALE = "female", "Female"

    datetime_create = None
    code = models.SlugField(max_length=250, unique=True, editable=False)
    is_ban = models.BooleanField(default=False)
    phone = models.CharField(max_length=10, unique=True, null=True, blank=True)
    gender = models.CharField(
        max_length=30,
        choices=GENDER_CHOICES.choices,
        default=GENDER_CHOICES.NOT_SELECTED,
    )
    avatar = models.ImageField(upload_to="images/User/Avatar", blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    reset_password_link = models.CharField(
        max_length=250, null=True, blank=True, editable=False
    )
    referral_code = models.CharField(max_length=15, null=True, blank=True)

    PHONE_FIELD = "phone"

    def get_code_token(self):
        return self.reset_password_link

    def save(self, *args, **kwargs):
        if not self.is_deleted:
            if not self.code or self.code is None:
                self.set_code()
            if not self.username or self.username is None:
                self.set_username()
            if not self.referral_code or self.referral_code is None:
                self.set_referral_code()
            super().save(*args, **kwargs)

    def get_role_display(self):
        return (
            "Super Admin" if self.is_superuser else "Admin" if self.is_staff else "User"
        )

    def get_avatar_tmb_url(self):
        return get_image_thumbnail(self.avatar)

    def get_is_active_display(self):
        return "On" if self.is_active else "Off"

    def get_is_ban_display(self):
        return "On" if self.is_ban else "Off"

    def get_language(self):
        return self.usersetting.language

    def get_language_str(self):
        return "EN - English" if self.usersetting.language == "en" else "FA - Persian"

    def get_light_dark_mode(self):
        return self.usersetting.is_dark_mode

    def get_background_theme(self):
        return self.usersetting.background_theme

    def set_code(self):
        self.code = tc.uniq_number_code(self)

    def set_referral_code(self):
        self.referral_code = tc.uniq_str_referral_code(self)

    def set_username(self, value=None):
        if value is None:
            email = self.email
            value = tc.uniq_slugify_username_rplc_space_dot(self, email)
        self.username = value

    def get_admin_detail_v1_url(self):
        return reverse("admin-v1-user-detail", kwargs={"slug": self.code})

    def get_admin_update_v1_url(self):
        return reverse("admin-v1-user-edit", kwargs={"slug": self.code})

    def __str__(self):
        return self.get_username()

    def set_password(self, raw_password):
        _with_salt_password = set_salt_password(raw_password)
        self.password = make_password(_with_salt_password)
        self._password = _with_salt_password

    def check_password(self, raw_password):
        """
        Return a boolean of whether the raw_password was correct. Handles
        hashing formats behind the scenes.
        """

        def setter(raw_password):
            _with_salt_password = set_salt_password(raw_password)
            self.set_password(_with_salt_password)
            # Password hash upgrades shouldn't be considered password changes.
            self._password = None
            self.save(update_fields=["password"])

        return check_password(set_salt_password(raw_password), self.password, setter)
