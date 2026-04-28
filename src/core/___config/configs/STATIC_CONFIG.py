from decouple import config

from ___utils.base_variables import BASE_DIR

USE_STATIC_ROOT = config("USE_STATIC_ROOT", cast=bool, default=False)

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "zstatic"]

if USE_STATIC_ROOT:
    STATIC_ROOT = config("STATIC_ROOT")

STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"
