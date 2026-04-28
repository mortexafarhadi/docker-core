import re


class UserAgentMiddleware:
    MOBILE_REGEX = re.compile(r"mobile|iphone|ipod|android.*mobile", re.I)
    TABLET_REGEX = re.compile(r"ipad|android(?!.*mobile)", re.I)
    BOT_REGEX = re.compile(r"bot|crawler|spider|crawling", re.I)

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ua = request.META.get("HTTP_USER_AGENT", "")
        ua_l = ua.lower()

        # ------------------
        # Device type
        # ------------------
        request.is_mobile = bool(self.MOBILE_REGEX.search(ua))
        request.is_tablet = bool(self.TABLET_REGEX.search(ua))
        request.is_desktop = not (request.is_mobile or request.is_tablet)

        # ------------------
        # OS detection
        # ------------------
        request.is_android = "android" in ua_l
        request.is_ios = any(x in ua_l for x in ("iphone", "ipad", "ipod"))
        request.is_windows = "windows nt" in ua_l
        request.is_mac = "mac os x" in ua_l and not request.is_ios
        request.is_linux = "linux" in ua_l and not request.is_android

        # ------------------
        # Browser detection
        # ------------------
        request.is_chrome = "chrome" in ua_l and "edg" not in ua_l and "opr" not in ua_l
        request.is_firefox = "firefox" in ua_l
        request.is_safari = "safari" in ua_l and not request.is_chrome
        request.is_edge = "edg" in ua_l
        request.is_opera = "opr" in ua_l or "opera" in ua_l
        request.is_ie = "msie" in ua_l or "trident" in ua_l

        # ------------------
        # In-App Browsers
        # ------------------
        request.is_telegram = "telegram" in ua_l
        request.is_instagram = "instagram" in ua_l
        request.is_whatsapp = "whatsapp" in ua_l
        request.is_in_app_browser = any(
            [request.is_telegram, request.is_instagram, request.is_whatsapp]
        )

        # ------------------
        # Bots & Crawlers
        # ------------------
        request.is_bot = bool(self.BOT_REGEX.search(ua))

        # ------------------
        # Feature detection (heuristic)
        # ------------------
        request.supports_webp = not request.is_ie
        request.supports_websocket = not request.is_ie
        request.supports_pwa = (
            request.is_chrome or request.is_edge or request.is_firefox
        )

        # ------------------
        # Old browser
        # ------------------
        request.is_old_browser = request.is_ie

        # ------------------
        # Metadata
        # ------------------
        request.user_agent_raw = ua
        request.device_family = (
            "mobile"
            if request.is_mobile
            else "tablet" if request.is_tablet else "desktop"
        )

        request.browser_family = (
            "chrome"
            if request.is_chrome
            else (
                "firefox"
                if request.is_firefox
                else (
                    "safari"
                    if request.is_safari
                    else (
                        "edge"
                        if request.is_edge
                        else (
                            "opera"
                            if request.is_opera
                            else "ie" if request.is_ie else "unknown"
                        )
                    )
                )
            )
        )

        request.os_family = (
            "android"
            if request.is_android
            else (
                "ios"
                if request.is_ios
                else (
                    "windows"
                    if request.is_windows
                    else (
                        "mac"
                        if request.is_mac
                        else "linux" if request.is_linux else "unknown"
                    )
                )
            )
        )

        return self.get_response(request)
