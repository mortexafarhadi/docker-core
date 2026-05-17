from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from _0_utils.views.base_view import TemplateView


@method_decorator(login_required, name="dispatch")
class DashboardView(TemplateView):
    template_name = "_2_panel_user/v1/dashboard.html"
