from decouple import config

USE_AUTH_PASSWORD_VALIDATORS = config(
    "USE_AUTH_PASSWORD_VALIDATORS", cast=bool, default=True
)
DEPLOYED = config("DEPLOYED", cast=bool, default=False)

REMEMBER_ME_DURATION = 5184000  # 2 month
SESSION_COOKIE_AGE = 1209600  # 2 week
if DEPLOYED:
    SESSION_COOKIE_AGE = 3600  # 1 hour
    REMEMBER_ME_DURATION = 1209600  # 2 week

AUTH_PASSWORD_VALIDATORS = (
    [
        {
            "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
        },
    ]
    if USE_AUTH_PASSWORD_VALIDATORS
    else []
)

USE_ALLAUTH_SERVICE = config("USE_ALLAUTH_SERVICE", cast=bool, default=False)
if USE_ALLAUTH_SERVICE:
    AUTHENTICATION_BACKENDS = [
        # Needed to login by username in Django admin, regardless of `allauth`
        "django.contrib.auth.backends.ModelBackend",
        # `allauth` specific authentication methods, such as login by email
        "allauth.account.auth_backends.AuthenticationBackend",
    ]

    # Provider specific settings
    SOCIALACCOUNT_PROVIDERS = {
        "google": {
            # For each OAuth based provider, either add a ``SocialApp``
            # (``socialaccount`` app) containing the required client
            # credentials, or list them here:
            "APP": {
                "client_id": config("GOOGLE_OAUTH_CLIENT_ID", default=""),
                "secret": config("GOOGLE_OAUTH_SECRET", default=""),
                "key": config("GOOGLE_OAUTH_KEY", default=""),
            }
        }
    }

    SOCIALACCOUNT_LOGIN_ON_GET = config(
        "GOOGLE_OAUTH_SOCIALACCOUNT_LOGIN_ON_GET", cast=bool, default=True
    )
    LOGIN_REDIRECT_URL = config("GOOGLE_OAUTH_LOGIN_REDIRECT_URL", default="dashboard")
    LOGOUT_REDIRECT_URL = config("GOOGLE_OAUTH_LOGOUT_REDIRECT_URL", default="/")
    ACCOUNT_SIGNUP_FIELDS = config(
        "GOOGLE_OAUTH_ACCOUNT_SIGNUP_FIELDS",
        default="email*,username*,password1*,password2*",
    ).split(",")
