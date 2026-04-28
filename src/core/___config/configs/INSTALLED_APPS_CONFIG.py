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
    "___utils",
    "__site_setting",
    "__site_setting._modules.header",
    "__site_setting._modules.footer",
    "__site_setting._modules.site_social_media",
    "__user",
    "__user._modules.register_user",
    "__user._modules.user_setting",
    "__user._modules.user_social_media",
    "_auth",
    "_panel_admin",
    "_panel_user",
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
