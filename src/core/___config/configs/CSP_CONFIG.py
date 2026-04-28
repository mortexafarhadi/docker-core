from decouple import config
from django.utils.csp import CSP

USE_CSP = config("USE_CSP", cast=bool, default=True)

SECURE_CSP = {
    "default-src": [CSP.SELF],
    "style-src": [CSP.SELF, CSP.NONCE],
    "script-src": [CSP.SELF, CSP.NONCE],
    "img-src": [
        CSP.SELF,
    ],
    "font-src": [CSP.SELF],
    # Ajax/WebSocket Connection
    "connect-src": [
        CSP.SELF,
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
