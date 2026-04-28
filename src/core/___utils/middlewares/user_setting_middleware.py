from django.conf import settings
from django.utils.translation import activate

from ___config.configs.LANGUAGES_CONFIG import (
    DEFAULT_LANGUAGE_CODE,
    DEFAULT_LANGUAGE_NAME,
    LANGUAGES_FLAG,
    DEFAULT_LANGUAGE_FLAG,
)
from ___utils.service.session_and_cookie_service import (
    get_session_key,
    get_cookie_key,
    set_cookie_key,
)
from __user._modules.user_setting.views.base.views import (
    get_user_setting_with_user_object,
    get_user_setting_objects,
)

DONT_HAVE_MIDDLEWARE_ADDRESSES = (
    "media",
    "static",
    "ckeditor5",
    "accounts",
    "faker",
    "set-main-setting",
)


class UserSettingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _path_info = str(getattr(request, "path_info", ""))
        if any(
            _path_info.startswith(f"/{prefix}/")
            for prefix in DONT_HAVE_MIDDLEWARE_ADDRESSES
        ):
            return self.get_response(request)

        user = request.user
        new_dic = {}
        _language = DEFAULT_LANGUAGE_CODE
        if user.is_authenticated:
            user_setting = get_user_setting_with_user_object(user)
            if user_setting is None:
                user_setting = get_user_setting_objects().create(user=user)
            _language = user_setting.language
            new_dic["is_dark_mode"] = user_setting.is_dark_mode
            new_dic["background_theme"] = user_setting.background_theme
            new_dic["color_theme"] = user_setting.color_theme
            new_dic["sidebar_mode"] = user_setting.sidebar_mode
        else:
            session_language = get_session_key(request, "language")
            _language = (
                session_language
                if session_language is not None
                else DEFAULT_LANGUAGE_CODE
            )
            session_dark_mode = get_session_key(request, "dark_mode")
            new_dic["is_dark_mode"] = (
                session_dark_mode if session_dark_mode is not None else False
            )
            session_theme = get_session_key(request, "background_theme")
            new_dic["background_theme"] = (
                session_theme if session_theme is not None else "bg-default"
            )
            session_color_theme = get_session_key(request, "color_theme")
            new_dic["color_theme"] = (
                session_color_theme if session_color_theme is not None else ""
            )
            session_sidebar_mode = get_session_key(request, "sidebar_mode")
            new_dic["sidebar_mode"] = (
                session_sidebar_mode
                if session_sidebar_mode is not None
                else "adminuiux-sidebar-standard"
            )

        _language = activate_language_from_path(_path_info, _language)
        _language_name = get_language_name(_language)
        _language_flag = get_language_flag(_language)
        new_dic["language"] = _language
        new_dic["language_name"] = _language_name
        new_dic["language_flag"] = _language_flag
        new_dic["direction"] = find_direction_from_language(_language)
        request.user_setting = new_dic
        response = self.get_response(request)
        if user.is_authenticated:
            dark_mode_value = "dark" if new_dic.get("is_dark_mode") else "light"
            dark_mode_cookie = get_cookie_key(request, "adminuiuxlayoutmode")
            if dark_mode_value != dark_mode_cookie:
                set_cookie_key(response, "adminuiuxlayoutmode", dark_mode_value)

            background_theme_value = new_dic.get("background_theme")
            background_theme_cookie = get_cookie_key(request, "adminuiuxbggradient")
            if background_theme_value != background_theme_cookie:
                set_cookie_key(response, "adminuiuxbggradient", background_theme_value)

            color_theme_value = new_dic.get("color_theme")
            color_theme_cookie = get_cookie_key(request, "adminuiuxtheme")
            if color_theme_value != color_theme_cookie:
                set_cookie_key(response, "adminuiuxtheme", color_theme_value)

            sidebar_mode_value = new_dic.get("sidebar_mode")
            sidebar_mode_cookie = get_cookie_key(request, "adminuiuxsidebarlayout")
            if sidebar_mode_value != sidebar_mode_cookie:
                set_cookie_key(response, "adminuiuxsidebarlayout", sidebar_mode_value)

        return response


def get_language_name(language_code):
    all_languages = getattr(settings, "LANGUAGES", [])
    for code, name in all_languages:
        if code == language_code:
            return name
    return DEFAULT_LANGUAGE_NAME


def get_language_flag(language_code):
    return LANGUAGES_FLAG.get(language_code, DEFAULT_LANGUAGE_FLAG)


def activate_language_from_path(
    path_info,
    current_language: str = None,
    fallback: str = DEFAULT_LANGUAGE_CODE,
):
    path = (path_info or "").lstrip("/")
    first_segment = path.split("/", 1)[0]

    valid_lang_codes = {code for code, _name in getattr(settings, "LANGUAGES", [])}

    target_language = first_segment if first_segment in valid_lang_codes else fallback
    if not current_language or not first_segment or current_language != target_language:
        activate(target_language)

    return target_language


def find_direction_from_language(language):
    try:
        language_direction = getattr(settings, "LANGUAGES_DIRECTION", {})
        if len(language_direction) == 0:
            return "ltr"
        return language_direction[language]
    except Exception as e:
        print(e)
        return "ltr"
