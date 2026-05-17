from django.urls import path, include

from _2_account.views.admin import views_base as vb
from _2_account.views.admin import views_user as vv

urlpatterns = [
    path("admin/", vv.AdminListView.as_view(), name="admin-v2-admin-list"),
    path(
        "customer/",
        vv.CustomerListView.as_view(),
        name="admin-v2-customer-list",
    ),
    path(
        "social-media/",
        include("_2_account._modules.user_social_media.urls.admin.v2.urls_i18n"),
    ),
    path(
        "register/",
        vv.RegisterListView.as_view(),
        name="admin-v2-register-list",
    ),
    path(
        "register/delete/",
        vv.RegisterDeleteView.as_view(),
        name="admin-v2-register-delete",
    ),
    path("delete/", vv.UserDeleteView.as_view(), name="admin-v2-user-delete"),
    path("staff/", vv.ToggleStaffView.as_view(), name="admin-v2-user-staff"),
    path("active/", vv.ToggleActiveView.as_view(), name="admin-v2-user-active"),
    path("ban/", vv.ToggleBanView.as_view(), name="admin-v2-user-ban"),
    path(
        "edit/<slug:slug>/",
        vv.UserEditView.as_view(),
        name="admin-v2-user-edit",
    ),
    path(
        "<slug:slug>/",
        vv.UserDetailView.as_view(),
        name="admin-v2-user-detail",
    ),
    path(
        "<user_code>/wallet-card/",
        include("apps.wallet._modules.wallet_card.urls.admin.v2.urls"),
    ),
    path(
        "<user_code>/transaction/deposit/",
        include("apps.wallet._modules.wallet_deposit.urls.admin.v2.urls"),
    ),
    path(
        "<user_code>/transaction/withdrawal/",
        include("apps.wallet._modules.wallet_withdrawal.urls.admin.v2.urls"),
    ),
    path("", vb.BaseUsersTemplateView.as_view(), name="admin-v2-user-template"),
]
