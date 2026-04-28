from ___utils.views.base_view import TemplateView
from __user.views.base.views_user import get_user_with_code


class WalletBalanceComponent(TemplateView):
    template_name_v1 = "wallet/admin/v1/component_wallet_balance.html"
    template_name_v2 = "wallet/admin/v2/component_wallet_balance.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_code = kwargs.get("user_code")
        wallet = get_user_with_code(user_code).wallet
        context["wallet"] = wallet
        return context
