from decouple import config

from ___utils.base_variables import BASE_DIR

USE_SQLITE_DB = config("USE_SQLITE_DB", cast=bool, default=True)

if USE_SQLITE_DB:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": config("DATABASES_ENGINE", default=""),
            "NAME": config("DATABASES_NAME", default=""),
            "USER": config("DATABASES_USERNAME", default=""),
            "PASSWORD": config("DATABASES_PASSWORD", default=""),
            "HOST": config("DATABASES_HOST", default=""),
            "PORT": config("DATABASES_PORT", default=""),
        }
    }
