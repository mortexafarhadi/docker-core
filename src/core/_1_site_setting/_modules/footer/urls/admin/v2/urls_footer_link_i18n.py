from django.urls import path

from ....views.admin import views_footer_link as vv

urlpatterns = [
    path(
        "add/",
        vv.FooterLinkCreateView.as_view(),
        name="admin-v2-setting-footer-link-add",
    ),
    path(
        "delete/",
        vv.FooterLinkDeleteView.as_view(),
        name="admin-v2-setting-footer-link-delete",
    ),
    path(
        "edit/<pk>/",
        vv.FooterLinkEditView.as_view(),
        name="admin-v2-setting-footer-link-edit",
    ),
    path(
        "<pk>/",
        vv.FooterLinkDetailView.as_view(),
        name="admin-v2-setting-footer-link-detail",
    ),
    path(
        "",
        vv.FooterLinkListView.as_view(),
        name="admin-v2-setting-footer-link-list",
    ),
]
