from django.urls import reverse

from _0_utils.views.base_view import ListView, DetailView, CreateView
from _1_user.views.base.views_user import get_user_with_code
from ...forms import forms as ff
from ...models import models as mm


class WalletDepositListView(ListView):
    template_name = "wallet_deposit/admin/wallet_deposit_list.html"
    model = mm.WalletDeposit

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


class WalletDepositDetailView(DetailView):
    template_name = "wallet_deposit/admin/wallet_deposit_detail.html"
    model = mm.WalletDeposit

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_code = self.kwargs.get("user_code")
        context["user_code"] = user_code
        return context


class WalletDepositCreateView(CreateView):
    template_name = "wallet_deposit/admin/wallet_deposit_edit.html"
    model = mm.WalletDeposit
    form_class = ff.WalletDepositForm
    my_success_url_v1 = "admin-v1-user-wallet-deposit:list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_code = self.kwargs.get("user_code")
        context["user_code"] = user_code
        return context

    def form_valid(self, form):
        user_code = self.kwargs.get("user_code")
        user_wallet = get_user_with_code(user_code).wallet
        form.instance.wallet = user_wallet
        amount = form.cleaned_data.get("amount")
        user_wallet.balance += amount
        user_wallet.save()
        return super().form_valid(form)

    def get_success_url(self):
        user_code = self.kwargs.get("user_code")
        if "_addanother" in self.request.POST:
            return reverse(
                "admin-v1-user-wallet-deposit:add",
                kwargs={"user_code": user_code},
            )
        else:
            return reverse(self.my_success_url_v1, kwargs={"user_code": user_code})
