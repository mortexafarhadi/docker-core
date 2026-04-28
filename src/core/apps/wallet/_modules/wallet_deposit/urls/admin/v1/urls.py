from django.urls import path

from ....views.admin import views as vv

app_name = "admin-v1-user-wallet-deposit"

urlpatterns = [
    path("add/", vv.WalletDepositCreateView.as_view(), name="add"),
    path("<pk>/", vv.WalletDepositDetailView.as_view(), name="detail"),
    path("", vv.WalletDepositListView.as_view(), name="list"),
]
