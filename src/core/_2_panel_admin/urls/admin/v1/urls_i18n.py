from django.urls import path, include

from _2_panel_admin.views.admin import views as vv

urlpatterns = [
    path("setting/", include("_1_site_setting.urls.admin.v1.urls_i18n")),
    path("user/", include("_2_account.urls.admin.v1.urls_i18n")),
    path("social-network/", include("apps.social_network.urls.admin.v1.urls_i18n")),
    path("category/", include("apps.category.urls.admin.v1.urls_i18n")),
    path("", vv.DashboardView.as_view(), name="admin-v1-dashboard"),
]
