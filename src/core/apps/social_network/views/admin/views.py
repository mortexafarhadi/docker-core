from django.shortcuts import redirect
from django.views.generic import View

from ___utils.views.base_view import (
    ListView,
    DetailView,
    UpdateView,
    CreateView,
)
from ..base.views import get_social_network_with_pk
from ...forms import forms as ff
from ...models import models as mm


class SocialNetworkListView(ListView):
    template_name_v1 = "social_network/admin/v1/social_network_list.html"
    template_name_v2 = "social_network/admin/v2/social_network_list.html"
    model = mm.SocialNetwork


class SocialNetworkDetailView(DetailView):
    template_name_v1 = "social_network/admin/v1/social_network_detail.html"
    template_name_v2 = "social_network/admin/v2/social_network_detail.html"
    model = mm.SocialNetwork


class SocialNetworkEditView(UpdateView):
    template_name_v1 = "social_network/admin/v1/social_network_edit.html"
    template_name_v2 = "social_network/admin/v2/social_network_edit.html"
    model = mm.SocialNetwork
    form_class = ff.SocialNetworkForm
    my_success_url_v1 = "admin-v1-social-network:detail"


class SocialNetworkCreateView(CreateView):
    template_name_v1 = "social_network/admin/v1/social_network_edit.html"
    template_name_v2 = "social_network/admin/v2/social_network_edit.html"
    model = mm.SocialNetwork
    form_class = ff.SocialNetworkForm
    my_success_url_v1 = "/panel-admin/social-network/"


class SocialNetworkDeleteView(View):
    def post(self, request):
        pk = request.POST.get("pk")
        get_social_network_with_pk(pk).delete()
        next_page = request.POST.get("next_page")
        if next_page[-6:] == "detail":
            return redirect(next_page, pk=pk)
        return redirect(next_page)
