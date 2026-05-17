from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import View

from _0_utils.views.base_view import ListView, DetailView, CreateView
from _1_user.views.base.views_user import get_user_with_code
from ..base.views import get_wallet_withdrawal_with_pk
from ...forms import forms as ff
from ...models import models as mm


class WalletWithdrawalListView(ListView):
    template_name = "wallet_withdrawal/user/wallet_withdrawal_list.html"
    model = mm.WalletWithdrawal
    ordering = ["-datetime_create"]

    def get_queryset(self):
        query = self.cached_queryset
        user_code = self.kwargs.get("user_code")
        query = query.filter(wallet__user__code__iexact=str(user_code))
        return query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_code = self.kwargs.get("user_code")
        context["user_code"] = user_code
        return context


class WalletWithdrawalDetailView(DetailView):
    template_name = "wallet_withdrawal/user/wallet_withdrawal_detail.html"
    model = mm.WalletWithdrawal

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_code = self.kwargs.get("user_code")
        context["user_code"] = user_code
        return context


# class WalletWithdrawalEditView(UpdateView):
#     template_name = 'wallet_withdrawal/admin/wallet_withdrawal_edit.html'
#     model = mm.WalletWithdrawal
#     form_class = ff.WalletWithdrawalForm
#     my_success_url_v1 = 'admin-wallet-withdrawal-detail'
#
#
class WalletWithdrawalCreateView(CreateView):
    template_name = "wallet_withdrawal/user/wallet_withdrawal_edit.html"
    model = mm.WalletWithdrawal
    form_class = ff.WalletWithdrawalForm
    success_url = "/panel-admin/wallet-withdrawal/"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        user_code = self.kwargs.get("user_code")
        wallet = get_user_with_code(user_code).wallet
        kwargs["wallet"] = wallet
        return kwargs

    def form_valid(self, form):
        user_code = self.kwargs.get("user_code")
        wallet = get_user_with_code(user_code).wallet
        form.instance.wallet = wallet
        response = super().form_valid(form)
        self.object.request_withdrawal(form.cleaned_data["amount"])
        return response

    def get_success_url(self):
        return reverse(
            "admin-v1-user-wallet-withdrawal:list",
            kwargs={"user_code": self.kwargs.get("user_code")},
        )


class WalletWithdrawalRejectView(View):
    def post(self, request, user_code):
        pk = request.POST.get("pk")
        rejection_reason = request.POST.get("description")
        wallet_withdrawal = get_wallet_withdrawal_with_pk(pk)
        wallet_withdrawal.set_rejected(rejection_reason)
        wallet_withdrawal.save()
        return redirect(
            "admin-v1-user-wallet-withdrawal:detail",
            user_code=user_code,
            pk=pk,
        )


class WalletWithdrawalPaymentQueueView(View):
    def post(self, request, user_code):
        pk = request.POST.get("pk")
        wallet_withdrawal = get_wallet_withdrawal_with_pk(pk)
        wallet_withdrawal.set_payment_queue()
        wallet_withdrawal.save()
        return redirect(
            "admin-v1-user-wallet-withdrawal:detail",
            user_code=user_code,
            pk=pk,
        )


class WalletWithdrawalCompletedView(View):
    def post(self, request, user_code):
        pk = request.POST.get("pk")
        wallet_withdrawal = get_wallet_withdrawal_with_pk(pk)
        wallet_withdrawal.set_completed()
        wallet_withdrawal.save()
        return redirect(
            "admin-v1-user-wallet-withdrawal:detail",
            user_code=user_code,
            pk=pk,
        )
