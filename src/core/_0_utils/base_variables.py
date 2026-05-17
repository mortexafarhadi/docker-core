from pathlib import Path

from decouple import config

APPLICATION_VERSION = "4.4.1"

BASE_DIR = Path(__file__).resolve().parent.parent
SHOW_LOG_DEBUG = config("SHOW_LOG_DEBUG", cast=bool, default=False)
USE_SMS_SERVICE = config("USE_SMS_SERVICE", cast=bool, default=False)
FRONT_DOMAIN_ADDRESS = config("FRONT_DOMAIN_ADDRESS", default=None)
