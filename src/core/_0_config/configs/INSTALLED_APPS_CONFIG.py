from decouple import config

from . import LANGUAGES_CONFIG

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    # EXTERNAL APP
    "django_cleanup.apps.CleanupConfig",
    "django_render_partial",
    "sorl.thumbnail",
    "simple_history",
    "jalali_date",
    "multiselectfield",
    "django_htmx",
    "django_ckeditor_5",
    "django_celery_beat",
    # 'captcha',
    # INTERNAL APP
    "_0_utils",
    "_1_site_setting",
    "_1_site_setting._modules.header",
    "_1_site_setting._modules.footer",
    "_1_site_setting._modules.site_social_media",
    "_1_user",
    "_1_user._modules.register_user",
    "_1_user._modules.user_setting",
    "_1_user._modules.user_social_media",
    "_2_auth",
    "_2_panel_admin",
    "_2_panel_user",
    "apps.wallet",
    "apps.wallet._modules.wallet_card",
    "apps.wallet._modules.wallet_deposit",
    "apps.wallet._modules.wallet_withdrawal",
    "apps.category",
    "apps.social_network",
]

if LANGUAGES_CONFIG.USE_MULTI_LANGUAGE:
    INSTALLED_APPS += [
        "translated_fields",
    ]

USE_ALLAUTH_SERVICE = config("USE_ALLAUTH_SERVICE", cast=bool, default=False)
if USE_ALLAUTH_SERVICE:
    INSTALLED_APPS += [
        "allauth",
        "allauth.account",
        "allauth.socialaccount",
        "allauth.socialaccount.providers.google",
    ]
