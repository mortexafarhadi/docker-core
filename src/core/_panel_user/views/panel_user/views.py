from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from ___utils.views.base_view import TemplateView


@method_decorator(login_required, name="dispatch")
class DashboardView(TemplateView):
    template_name = "_panel_user/v1/dashboard.html"
