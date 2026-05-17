from django.http import JsonResponse
from django.shortcuts import redirect
from django.utils.translation import activate
from django.views.generic import View

from _0_config.configs.LANGUAGES_CONFIG import USE_MULTI_LANGUAGE
from _0_utils.service.session_and_cookie_service import (
    set_session_key,
    get_cookie_key,
)


class ChangeLanguageView(View):
    def post(self, request):
        language = request.POST.get("language")
        next_url = request.POST.get("next_url")
        if USE_MULTI_LANGUAGE:
            next_url = f"/{language}/{next_url[4:]}"
        user = request.user
        if user.is_authenticated:
            user_setting = user.usersetting
            user_setting.language = language
            user_setting.save()
        else:
            if language and language is not None:
                set_session_key(request, "language", language)
        activate(language)
        return redirect(next_url)


class ToggleDarkModeStatusView(View):
    def post(self, request):
        user = request.user
        if user.is_authenticated:
            setting = user.usersetting
            setting.is_dark_mode = (
                True
                if get_cookie_key(request, "adminuiuxlayoutmode") == "dark"
                else False
            )
            setting.save()
        return JsonResponse({"result": "ok"})


class ChangeBackgroundModeView(View):
    def post(self, request):
        user = request.user
        if user.is_authenticated:
            setting = user.usersetting
            setting.background_theme = get_cookie_key(request, "adminuiuxbggradient")
            setting.save()
        return JsonResponse({"result": "ok"})


class ChangeColorModeView(View):
    def post(self, request):
        user = request.user
        if user.is_authenticated:
            setting = user.usersetting
            setting.color_theme = get_cookie_key(request, "adminuiuxtheme")
            setting.save()
        return JsonResponse({"result": "ok"})


class ChangeSidebarModeView(View):
    def post(self, request):
        user = request.user
        if user.is_authenticated:
            setting = user.usersetting
            setting.sidebar_mode = get_cookie_key(request, "adminuiuxsidebarlayout")
            setting.save()
        return JsonResponse({"result": "ok"})
