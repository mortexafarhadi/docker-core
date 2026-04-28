from decouple import config
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from ..configs import LANGUAGES_CONFIG

# from django.conf.urls import handler404
from django.urls import path, include, re_path
from django.views.generic import RedirectView
from django.views.static import serve

urlpatterns = [
    path(
        "ckeditor5/", include("django_ckeditor_5.urls"), name="ck_editor_5_upload_file"
    ),
]
i18n_paths = [
    path("v1/auth/", include("_auth.urls.v1.urls")),
    path("v2/auth/", include("_auth.urls.v2.urls")),
]

USE_PANEL_ADMIN_DJANGO = config("USE_PANEL_ADMIN_DJANGO", cast=bool, default=False)
if USE_PANEL_ADMIN_DJANGO:
    i18n_paths += [
        path("admin/", admin.site.urls),
    ]

USE_PANEL_ADMIN_CUSTOM = config("USE_PANEL_ADMIN_CUSTOM", cast=bool, default=True)
if USE_PANEL_ADMIN_CUSTOM:
    i18n_paths += [
        path("panel-admin/", RedirectView.as_view(url="/v1/panel-admin/")),
        path("v1/panel-admin/", include("_panel_admin.urls.admin.v1.urls_i18n")),
        path("v2/panel-admin/", include("_panel_admin.urls.admin.v2.urls_i18n")),
    ]

USE_PANEL_USER = config("USE_PANEL_USER", cast=bool, default=True)
if USE_PANEL_USER:
    i18n_paths += [
        path("user/", RedirectView.as_view(url="/v1/user/")),
        path("v1/user/", include("_panel_user.urls.panel_user.v1.urls_i18n")),
        path("v2/user/", include("_panel_user.urls.panel_user.v2.urls_i18n")),
    ]

if not USE_PANEL_ADMIN_DJANGO and not USE_PANEL_ADMIN_CUSTOM:
    i18n_paths += [
        path("panel-admin/", RedirectView.as_view(url="/v1/panel-admin/")),
        path("v1/panel-admin/", include("_panel_admin.urls.admin.v1.urls_i18n")),
        path("v2/panel-admin/", include("_panel_admin.urls.admin.v2.urls_i18n")),
    ]

USE_ALLAUTH_SERVICE = config("USE_ALLAUTH_SERVICE", cast=bool, default=False)
if USE_ALLAUTH_SERVICE:
    urlpatterns += [
        path("accounts/", include("allauth.urls")),
    ]

USE_FAKER_URL = config("USE_FAKER_URL", cast=bool, default=False)
if USE_FAKER_URL:
    urlpatterns += [
        path("faker/", include("_fake_data.urls")),
    ]

SERVE_MEDIA_STATIC = config("SERVE_MEDIA_STATIC", cast=bool, default=False)
if SERVE_MEDIA_STATIC:
    urlpatterns += [
        re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
        re_path(
            r"^static/(?P<path>.*)$", serve, {"document_root": settings.STATIC_ROOT}
        ),
    ]

urlpatterns += [
    path("set-user-setting/", include("__user._modules.user_setting.urls.urls")),
]
i18n_paths += [
    path("", include("__site_setting.urls.base.urls_i18n")),
]

urlpatterns += (
    i18n_patterns(*i18n_paths) if LANGUAGES_CONFIG.USE_MULTI_LANGUAGE else i18n_paths
)
