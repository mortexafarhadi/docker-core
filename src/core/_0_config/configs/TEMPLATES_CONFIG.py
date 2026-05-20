from _0_utils.base_variables import BASE_DIR
from . import CSP_CONFIG

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "ztemplates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                *(
                    ["django.template.context_processors.csp"]
                    if CSP_CONFIG.USE_CSP
                    else []
                ),
            ],
        },
    },
]
