from decouple import config
from django.utils.csp import CSP

USE_CSP = config("USE_CSP", cast=bool, default=True)

SECURE_CSP = (
    None
    if not USE_CSP
    else {
        "default-src": [CSP.SELF],
        "style-src": [
            CSP.SELF,
            CSP.NONCE,
            "https://fonts.googleapis.com",
        ],
        "script-src": [
            CSP.SELF,
            CSP.NONCE,
            "https://cdn.jsdelivr.net",
            "https://unpkg.com",
            "'wasm-unsafe-eval'",
        ],
        "img-src": [
            CSP.SELF,
            "data:",
        ],
        "font-src": [
            CSP.SELF,
            "data:",
            "https://fonts.gstatic.com",
            "https://unpkg.com",
            "https://cdn.jsdelivr.net",
        ],
        # Ajax/WebSocket Connection
        "connect-src": [
            CSP.SELF,
            "https://cdn.jsdelivr.net",
            "https://unpkg.com",
        ],
        "frame-src": [
            CSP.SELF,
        ],
        # Video/Audio
        "media-src": [
            CSP.SELF,
        ],
        # Plugins like (flash, ...)
        "object-src": [
            CSP.SELF,
        ],
        "base-uri": [
            CSP.SELF,
        ],
        "form-action": [
            CSP.SELF,
        ],
        # who can embed your site
        "frame-ancestors": [
            CSP.SELF,
        ],
    }
)
