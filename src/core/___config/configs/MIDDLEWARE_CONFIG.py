from decouple import config

from . import LANGUAGES_CONFIG, CSP_CONFIG

MIDDLEWARE = [
    # EXTERNAL MIDDLEWARE
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
]
if LANGUAGES_CONFIG.USE_MULTI_LANGUAGE:
    MIDDLEWARE += [
        "django.middleware.locale.LocaleMiddleware",
    ]
if CSP_CONFIG.USE_CSP:
    MIDDLEWARE += [
        "django.middleware.csp.ContentSecurityPolicyMiddleware",
    ]

MIDDLEWARE += [
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "simple_history.middleware.HistoryRequestMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
    # INTERNAL MIDDLEWARE
    "___utils.middlewares.ip_address_middleware.IPAddressMiddleware",
    "___utils.middlewares.request_params_middleware.RequestParamsMiddleware",
    "___utils.middlewares.user_setting_middleware.UserSettingMiddleware",
    "___utils.middlewares.user_agent_middleware.UserAgentMiddleware",
]

USE_ALLAUTH_SERVICE = config("USE_ALLAUTH_SERVICE", cast=bool, default=False)
if USE_ALLAUTH_SERVICE:
    MIDDLEWARE += [
        "allauth.account.middleware.AccountMiddleware",
    ]

USE_ADMIN_ACCESS_MIDDLEWARE = config(
    "USE_ADMIN_ACCESS_MIDDLEWARE", cast=bool, default=True
)
if USE_ADMIN_ACCESS_MIDDLEWARE:
    MIDDLEWARE += [
        "___utils.middlewares.access_middleware.AdminAccessMiddleware",
    ]
