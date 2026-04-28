from django.urls import path

from ....views.admin import views_footer_link_group as vv

urlpatterns = [
    path(
        "add/",
        vv.FooterLinkGroupCreateView.as_view(),
        name="admin-v1-setting-footer-group-add",
    ),
    path(
        "delete/",
        vv.FooterLinkGroupDeleteView.as_view(),
        name="admin-v1-setting-footer-group-delete",
    ),
    path(
        "edit/<pk>/",
        vv.FooterLinkGroupEditView.as_view(),
        name="admin-v1-setting-footer-group-edit",
    ),
    path(
        "<pk>/",
        vv.FooterLinkGroupDetailView.as_view(),
        name="admin-v1-setting-footer-group-detail",
    ),
    path(
        "",
        vv.FooterLinkGroupListView.as_view(),
        name="admin-v1-setting-footer-group-list",
    ),
]
