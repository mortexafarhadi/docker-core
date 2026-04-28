from django.urls import path

from ....views.admin import views as vv

app_name = "admin-v1-user-wallet-card"

urlpatterns = [
    path("add/", vv.WalletCardCreateView.as_view(), name="add"),
    path("delete/", vv.WalletCardDeleteView.as_view(), name="delete"),
    path("edit/<pk>/", vv.WalletCardEditView.as_view(), name="edit"),
    path("<pk>/", vv.WalletCardDetailView.as_view(), name="detail"),
    path("", vv.WalletCardListView.as_view(), name="list"),
]
