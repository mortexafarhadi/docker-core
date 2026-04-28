from decouple import config

from ___utils.base_variables import BASE_DIR

USE_MEDIA_ROOT = config("USE_MEDIA_ROOT", cast=bool, default=False)

MEDIA_ROOT = config("MEDIA_ROOT") if USE_MEDIA_ROOT else BASE_DIR / "zmedias"
MEDIA_URL = "/media/"
