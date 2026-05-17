from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import View

from _0_utils.templatetags.poll_extras import separate_with_dash
from _0_utils.views.base_view import ListView, DetailView, FormView, render
from _1_user.views.base.views_user import get_user_with_code
from ..base.views import get_wallet_card_with_pk
from ...forms import forms as ff
from ...models import models as mm


class WalletCardListView(ListView):
    template_name = "wallet_card/admin/wallet_card_list.html"
    model = mm.WalletCard

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


class WalletCardDetailView(DetailView):
    template_name = "wallet_card/admin/wallet_card_detail.html"
    model = mm.WalletCard


class WalletCardEditView(View):
    template_name = "wallet_card/admin/wallet_card_edit.html"
    my_success_url_v1 = "admin-v1-user-wallet-card:detail"

    def get(self, request, user_code, pk, *args, **kwargs):
        object = get_wallet_card_with_pk(pk)
        form = ff.WalletCardForm(
            initial={
                "bank_name": object.bank_name,
                "card_number": separate_with_dash(object.card_number),
                "shaba_number": separate_with_dash(object.shaba_number),
            }
        )
        context = {"object": object, "form": form}
        return render(request, self.template_name, context)

    def post(self, request, user_code, pk, *args, **kwargs):
        object = get_wallet_card_with_pk(pk)
        form = ff.WalletCardForm(request.POST)
        if form.is_valid():
            bank_name = form.cleaned_data.get("bank_name")
            card_number = form.cleaned_data.get("card_number")
            card_number = card_number.replace("-", "")
            card_number = card_number.replace(" ", "")
            if len(card_number) != 16:
                form.add_error("card_number", "card number must be 16 digits")
            shaba_number = form.cleaned_data.get("shaba_number")
            shaba_number = shaba_number.replace("-", "")
            shaba_number = shaba_number.replace(" ", "")
            if len(shaba_number) <= 20:
                form.add_error("shaba_number", "Shaba number is not valid")
            if not form.has_error("card_number") and not form.has_error("shaba_number"):
                object.card_number = card_number
                object.shaba_number = shaba_number
                object.bank_name = bank_name
                object.save()
                return redirect(self.my_success_url_v1)

        context = {"object": object, "form": form}
        return render(request, self.template_name, context)


class WalletCardCreateView(FormView):
    template_name = "wallet_card/admin/wallet_card_edit.html"
    form_class = ff.WalletCardForm
    my_success_url = "admin-user-wallet-card-list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_code = self.kwargs.get("user_code")
        context["user_code"] = user_code
        return context

    def form_valid(self, form):
        user_code = self.kwargs.get("user_code")
        bank_name = form.cleaned_data.get("bank_name")
        card_number = form.cleaned_data.get("card_number")
        card_number = card_number.replace("-", "")
        card_number = card_number.replace(" ", "")
        if len(card_number) != 16:
            form.add_error("card_number", "card number must be 16 digits")
        shaba_number = form.cleaned_data.get("shaba_number")
        shaba_number = shaba_number.replace("-", "")
        shaba_number = shaba_number.replace(" ", "")
        if len(shaba_number) <= 20:
            form.add_error("shaba_number", "Shaba number is not valid")
        if form.has_error("card_number") or form.has_error("shaba_number"):
            return super().form_invalid(form)
        wallet = get_user_with_code(user_code).wallet
        wallet.walletcard_set.create(
            card_number=card_number,
            shaba_number=shaba_number,
            bank_name=bank_name,
        )
        return super().form_valid(form)

    def get_success_url(self):
        user_code = self.kwargs.get("user_code")
        if "_addanother" in self.request.POST:
            return reverse(
                "admin-user-wallet-card-add", kwargs={"user_code": user_code}
            )
        else:
            return reverse(self.my_success_url, kwargs={"user_code": user_code})


class WalletCardDeleteView(View):
    def post(self, request):
        pk = request.POST.get("pk")
        get_wallet_card_with_pk(pk).delete()
        next_page = request.POST.get("next_page")
        if next_page[-6:] == "detail":
            return redirect(next_page, pk=pk)
        return redirect(next_page)
