from decouple import config

DEPLOYED = config("DEPLOYED", cast=bool, default=False)
DJANGO_PORT = config("DJANGO_PORT", default="8000")
USE_SSL_CONFIG = config("USE_SSL_CONFIG", cast=bool, default=True)


def get_media_domain_url():
    from _0_config.settings import ALLOWED_HOSTS

    if ALLOWED_HOSTS and ALLOWED_HOSTS != "*":
        for host in ALLOWED_HOSTS:
            if not host.startswith("http"):
                return host
    return f"http://127.0.0.1:{DJANGO_PORT}"


def base_url():
    if DEPLOYED:
        protocol = "https" if USE_SSL_CONFIG else "http"
        return f"{protocol}://{get_media_domain_url()}"
    else:
        return f"http://127.0.0.1:{DJANGO_PORT}"


def media_url(data):
    if not data:
        return None
    data = str(data)
    if not data.strip():
        return None
    return f"{base_url()}{data}"
