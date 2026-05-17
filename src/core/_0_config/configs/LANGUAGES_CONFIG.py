from decouple import config

USE_MULTI_LANGUAGE = config("USE_MULTI_LANGUAGE", cast=bool, default=False)
LANGUAGE_CODE = config("LANGUAGE_CODE", default="en-us")

if USE_MULTI_LANGUAGE:
    LANGUAGES = [
        ("en", "English"),
        ("fa", "Persian"),
    ]
    LANGUAGES_DIRECTION = {
        "en": "ltr",
        "fa": "rtl",
    }
    LANGUAGES_FLAG = {
        "fa": "flag-iran.png",
        "en": "flag-img1.png",
    }
    DEFAULT_LANGUAGE_CODE = LANGUAGES[0][0]
    DEFAULT_LANGUAGE_NAME = LANGUAGES[0][1]
    DEFAULT_LANGUAGE_FLAG = LANGUAGES_FLAG.get(DEFAULT_LANGUAGE_CODE)
else:
    if LANGUAGE_CODE == "en-us":
        DEFAULT_LANGUAGE_CODE = "en-us"
        DEFAULT_LANGUAGE_NAME = "English"
        DEFAULT_LANGUAGE_FLAG = "flag-img1.png"
    else:
        DEFAULT_LANGUAGE_CODE = "fa"
        DEFAULT_LANGUAGE_NAME = "Persian"
        DEFAULT_LANGUAGE_FLAG = "flag-iran.png"
