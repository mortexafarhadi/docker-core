from decouple import config

# ####  ZARINPAL  ####
USE_PAYMENT_SERVICE = config("USE_PAYMENT_SERVICE", default=True, cast=bool)
ZARINPAL_MERCHANT_ID = config("ZARINPAL_MERCHANT_ID", default=None)
ZARINPAL_SANDBOX = config("ZARINPAL_SANDBOX", default=False, cast=bool)
ZARINPAL_IS_TOMAN = config("ZARINPAL_IS_TOMAN", default=True, cast=bool)
ZARINPAL_CALLBACK_URL = config("ZARINPAL_CALLBACK_URL", default=None)
ZARINPAL_CALLBACK_URL_SANDBOX = config("ZARINPAL_CALLBACK_URL_SANDBOX", default=None)
SITE_FEE_PAYMENT = config("SITE_FEE_PAYMENT", default=29000, cast=int)
