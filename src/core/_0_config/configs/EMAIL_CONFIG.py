from decouple import config

USE_EMAIL_SERVICE = config("USE_EMAIL_SERVICE", cast=bool, default=False)

# ##### EMAIL SETTING ##### #
if USE_EMAIL_SERVICE:
    EMAIL_BACKEND = config("EMAIL_BACKEND")
    EMAIL_HOST = config("EMAIL_HOST", default="smtp4dev")
    EMAIL_PORT = config("EMAIL_PORT", cast=int, default=25)
    EMAIL_HOST_USER = config("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
    EMAIL_USE_TLS = config("EMAIL_USE_TLS", cast=bool, default=False)
    EMAIL_USE_SSL = config("EMAIL_USE_SSL", cast=bool, default=False)
    DEFAULT_FROM_EMAIL = config("EMAIL_SEND_FROM", default=EMAIL_HOST_USER)
