from django.urls import path, include
from __site_setting.views.admin import views_base as vv

urlpatterns = [
    path("site/", include("__site_setting.urls.admin.v2.urls_site")),
    path(
        "header-link/",
        include("__site_setting._modules.header.urls.admin.v2.urls_header_link_i18n"),
    ),
    path(
        "header-group/",
        include(
            "__site_setting._modules.header.urls.admin.v2.urls_header_link_group_i18n"
        ),
    ),
    path(
        "footer-group/",
        include(
            "__site_setting._modules.footer.urls.admin.v2.urls_footer_link_group_i18n"
        ),
    ),
    path(
        "footer-link/",
        include("__site_setting._modules.footer.urls.admin.v2.urls_footer_link_i18n"),
    ),
    path(
        "",
        vv.BaseSettingTemplateView.as_view(),
        name="admin-v2-setting-template",
    ),
]
