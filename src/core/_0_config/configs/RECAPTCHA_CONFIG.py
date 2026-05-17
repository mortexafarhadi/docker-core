from decouple import config

USE_RECAPTCHA = config("USE_RECAPTCHA", cast=bool, default=False)

if USE_RECAPTCHA:  # ##### CAPTCHA VARIABLE FOR DEPLOY ##### #
    RECAPTCHA_PUBLIC_KEY = config("RECAPTCHA_PUBLIC_KEY")
    RECAPTCHA_PRIVATE_KEY = config("RECAPTCHA_PRIVATE_KEY")
else:
    RECAPTCHA_PUBLIC_KEY = ""
    RECAPTCHA_PRIVATE_KEY = ""
