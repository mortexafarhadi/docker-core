from django.urls import path

from ....views.admin import views_header_link as vv

urlpatterns = [
    path(
        "add/",
        vv.HeaderLinkCreateView.as_view(),
        name="admin-v1-setting-header-link-add",
    ),
    path(
        "delete/",
        vv.HeaderLinkDeleteView.as_view(),
        name="admin-v1-setting-header-link-delete",
    ),
    path(
        "edit/<pk>/",
        vv.HeaderLinkEditView.as_view(),
        name="admin-v1-setting-header-link-edit",
    ),
    path(
        "<pk>/",
        vv.HeaderLinkDetailView.as_view(),
        name="admin-v1-setting-header-link-detail",
    ),
    path(
        "",
        vv.HeaderLinkListView.as_view(),
        name="admin-v1-setting-header-link-list",
    ),
]
