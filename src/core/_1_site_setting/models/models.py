from django.db import models
from django.urls import reverse

from _0_utils.functions.generator.file_path_generator import UploadPathFactory
from _0_utils.functions.generator.url_Image_setting import (
    get_image_thumbnail_setting,
)
from _0_utils.models import basic_models as mb


class SiteSetting(mb.BasicCKEditorModelHistorical):
    class SITE_TYPES_CHOICES(models.TextChoices):
        MAIN = (
            "main",
            "Main Website / User Panel",
        )
        ADMIN = (
            "admin",
            "Admin Panel",
        )
        LANDING = "landing", "Landing / Introduction"

    site_type = models.CharField(
        max_length=20,
        choices=SITE_TYPES_CHOICES,
        default=SITE_TYPES_CHOICES.MAIN,
        db_index=True,
    )
    # ########## Head Start ########## #
    section_head_title = models.CharField(max_length=200, default="MORTEXA")
    section_head_description = models.TextField(null=True, blank=True, default="")
    section_head_keywords = models.TextField(null=True, blank=True, default="")
    section_head_author = models.TextField(null=True, blank=True, default="")
    section_head_favicon = models.ImageField(
        upload_to=UploadPathFactory(
            base_path="media/Setting", subfolder="section_head_favicon"
        ),
        null=True,
        blank=True,
    )
    section_head_html_language = models.CharField(
        max_length=10, default="zxx", null=True, blank=True
    )
    # ########## Head End ########## #

    # ########## Base Start ########## #
    site_name = models.CharField(max_length=200, default="MORTEXA")
    link = models.URLField(default="http://127.0.0.1:8000/", null=True, blank=True)
    email = models.EmailField(
        default="contact@mortexafarhadi.com", null=True, blank=True
    )
    phone = models.CharField(
        max_length=20, default="+989910943896", null=True, blank=True
    )
    fax = models.CharField(max_length=20, default="+1234567890", null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    verify_code_digits = models.PositiveSmallIntegerField(default=5)
    thumbnail_quality = models.PositiveSmallIntegerField(default=70)
    thumbnail_size = models.CharField(
        max_length=10, default="512x512", null=True, blank=True
    )
    has_preloader = models.BooleanField(default=True)
    # ########## Base End ########## #

    logo_header = models.ImageField(
        upload_to=UploadPathFactory(base_path="media/Setting", subfolder="logo_header"),
        null=True,
        blank=True,
    )
    logo_footer = models.ImageField(
        upload_to=UploadPathFactory(base_path="media/Setting", subfolder="logo_footer"),
        null=True,
        blank=True,
    )
    logo_preload = models.ImageField(
        upload_to=UploadPathFactory(
            base_path="media/Setting", subfolder="logo_preload"
        ),
        null=True,
        blank=True,
    )
    footer_description = models.TextField(
        default="""The point of using Lorem Ipsum is that it has a more-or-less normal distribution of
                            letters, as opposed to using 'Content here, content here', making it look like readable
                            English. Many desktop publishing packages and web page editors now use Lorem Ipsum as
                            their default model text, and a search for 'lorem ipsum' will uncover many web sites
                            still in their infancy. Various versions have evolved over the years, sometimes by
                            accident, sometimes on purpose (injected humour and the like).""",
        null=True,
        blank=True,
    )
    footer_link_1_active = models.BooleanField(default=True)
    footer_link_1_text = models.CharField(
        max_length=250, default="Help", null=True, blank=True
    )
    footer_link_1_url = models.URLField(
        default="https://mortexafarhadi.com/", null=True, blank=True
    )
    footer_link_2_active = models.BooleanField(default=True)
    footer_link_2_text = models.CharField(
        max_length=250, default="Terms of Use", null=True, blank=True
    )
    footer_link_2_url = models.URLField(
        default="https://mortexafarhadi.com/", null=True, blank=True
    )
    footer_link_3_active = models.BooleanField(default=True)
    footer_link_3_text = models.CharField(
        max_length=250, default="Privacy Policy", null=True, blank=True
    )
    footer_link_3_url = models.URLField(
        default="https://mortexafarhadi.com/", null=True, blank=True
    )
    copyright_main_text_1 = models.TextField(
        default="© Developed by", null=True, blank=True
    )
    copyright_main_text_2 = models.TextField(default="@MORTEXA", null=True, blank=True)
    copyright_main_link_text = models.CharField(
        max_length=250, default="mortexafarhadi.com", null=True, blank=True
    )
    copyright_main_link_url = models.URLField(
        default="https://mortexafarhadi.com/", null=True, blank=True
    )
    copyright_auth_text_1 = models.TextField(
        default="© Developed by", null=True, blank=True
    )
    copyright_auth_text_2 = models.TextField(default="@MORTEXA", null=True, blank=True)
    copyright_auth_link_text = models.CharField(
        max_length=250, default="mortexafarhadi.com", null=True, blank=True
    )
    copyright_auth_link_url = models.URLField(
        default="https://mortexafarhadi.com/", null=True, blank=True
    )
    copyright_panels_text_1 = models.TextField(
        default="© Developed by", null=True, blank=True
    )
    copyright_panels_text_2 = models.TextField(
        default="@MORTEXA ❤️", null=True, blank=True
    )
    copyright_panels_link_text = models.CharField(
        max_length=250, default="mortexafarhadi.com", null=True, blank=True
    )
    copyright_panels_link_url = models.URLField(
        default="https://mortexafarhadi.com/", null=True, blank=True
    )
    sort_order = models.PositiveSmallIntegerField(default=1)
    is_main = models.BooleanField(default=True)

    def get_admin_detail_url(self):
        return reverse("admin-v1-setting-site:detail", kwargs={"pk": self.pk})

    def get_admin_update_url(self):
        return reverse("admin-v1-setting-site:edit", kwargs={"pk": self.pk})

    def get_address(self):
        return self.address if self.address and len(self.address) > 0 else "-----"

    def get_footer_description(self):
        return (
            self.footer_description
            if self.footer_description and len(self.footer_description) > 0
            else "-----"
        )

    def get_copyright_main_text_1(self):
        return (
            self.copyright_main_text_1
            if self.copyright_main_text_1 and len(self.copyright_main_text_1) > 0
            else "-----"
        )

    def get_copyright_main_text_2(self):
        return (
            self.copyright_main_text_2
            if self.copyright_main_text_2 and len(self.copyright_main_text_2) > 0
            else "-----"
        )

    def get_copyright_auth_text_1(self):
        return (
            self.copyright_auth_text_1
            if self.copyright_auth_text_1 and len(self.copyright_auth_text_1) > 0
            else "-----"
        )

    def get_copyright_auth_text_2(self):
        return (
            self.copyright_auth_text_2
            if self.copyright_auth_text_2 and len(self.copyright_auth_text_2) > 0
            else "-----"
        )

    def get_copyright_panels_text_1(self):
        return (
            self.copyright_panels_text_1
            if self.copyright_panels_text_1 and len(self.copyright_panels_text_1) > 0
            else "-----"
        )

    def get_copyright_panels_text_2(self):
        return (
            self.copyright_panels_text_2
            if self.copyright_panels_text_2 and len(self.copyright_panels_text_2) > 0
            else "-----"
        )

    def get_logo_header_tmb_url(self):
        return get_image_thumbnail_setting(self.logo_header)

    def get_logo_footer_tmb_url(self):
        return get_image_thumbnail_setting(self.logo_footer)

    def get_section_head_favicon_tmb_url(self):
        return get_image_thumbnail_setting(self.section_head_favicon)

    def get_logo_preload_tmb_url(self):
        return get_image_thumbnail_setting(self.logo_preload)

    def get_is_main(self):
        return "On" if self.is_main else "Off"

    def delete(self, *args, **kwargs):
        self.is_main = False
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.site_name
