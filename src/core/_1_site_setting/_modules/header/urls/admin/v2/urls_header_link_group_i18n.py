from django.urls import path

from ....views.admin import views_header_link_group as vv

urlpatterns = [
    path(
        "add/",
        vv.HeaderLinkGroupCreateView.as_view(),
        name="admin-v2-setting-header-group-add",
    ),
    path(
        "delete/",
        vv.HeaderLinkGroupDeleteView.as_view(),
        name="admin-v2-setting-header-group-delete",
    ),
    path(
        "edit/<pk>/",
        vv.HeaderLinkGroupEditView.as_view(),
        name="admin-v2-setting-header-group-edit",
    ),
    path(
        "<pk>/",
        vv.HeaderLinkGroupDetailView.as_view(),
        name="admin-v2-setting-header-group-detail",
    ),
    path(
        "",
        vv.HeaderLinkGroupListView.as_view(),
        name="admin-v2-setting-header-group-list",
    ),
]
