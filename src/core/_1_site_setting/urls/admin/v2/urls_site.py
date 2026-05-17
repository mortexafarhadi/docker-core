from django.urls import path

from _1_site_setting.views.admin import views_site as vv

app_name = "admin-v2-setting-site"

urlpatterns = [
    path("add/", vv.SiteSettingCreateView.as_view(), name="add"),
    path("delete/", vv.SiteSettingDeleteView.as_view(), name="delete"),
    path("edit/<pk>/", vv.SiteSettingEditView.as_view(), name="edit"),
    path("<pk>/", vv.SiteSettingDetailView.as_view(), name="detail"),
    path("", vv.SiteSettingListView.as_view(), name="list"),
]
