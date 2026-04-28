from decouple import config
from . import LANGUAGES_CONFIG

# ##### CODE SETTING BASE ##### #
LANGUAGE_CODE = config("LANGUAGE_CODE", default="en-us")
TIME_ZONE = config("TIME_ZONE", default="Asia/Tehran")
USE_I18N = config("USE_I18N", cast=bool, default=True)
USE_TZ = config("USE_TZ", cast=bool, default=True)

if LANGUAGES_CONFIG.USE_MULTI_LANGUAGE:
    USE_I18N = True
