from django.urls import path

from ....views.admin import views as vv

app_name = "admin-v1-user-wallet-withdrawal"

urlpatterns = [
    path("request/", vv.WalletWithdrawalCreateView.as_view(), name="add"),
    path("reject/", vv.WalletWithdrawalRejectView.as_view(), name="reject"),
    path(
        "payment-queue/",
        vv.WalletWithdrawalPaymentQueueView.as_view(),
        name="payment-queue",
    ),
    path("completed/", vv.WalletWithdrawalCompletedView.as_view(), name="completed"),
    path("<pk>/", vv.WalletWithdrawalDetailView.as_view(), name="detail"),
    path("", vv.WalletWithdrawalListView.as_view(), name="list"),
]
