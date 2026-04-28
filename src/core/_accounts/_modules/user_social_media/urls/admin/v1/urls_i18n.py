from django.urls import path

from ....views.admin import views as vv

urlpatterns = [
    path(
        "add/",
        vv.UserSocialMediaCreateView.as_view(),
        name="admin-v1-user-social-media-add",
    ),
    path(
        "delete/",
        vv.UserSocialMediaDeleteView.as_view(),
        name="admin-v1-user-social-media-delete",
    ),
    path(
        "edit/<pk>/",
        vv.UserSocialMediaEditView.as_view(),
        name="admin-v1-user-social-media-edit",
    ),
    path(
        "<pk>/",
        vv.UserSocialMediaDetailView.as_view(),
        name="admin-v1-user-social-media-detail",
    ),
    path(
        "",
        vv.UserSocialMediaListView.as_view(),
        name="admin-v1-user-social-media-list",
    ),
]
