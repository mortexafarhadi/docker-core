from django.shortcuts import redirect
from django.views.generic import View

from ___utils.views.base_view import (
    ListView,
    DetailView,
    UpdateView,
    CreateView,
)
from ..base.views_footer_link import get_footer_link_with_pk
from ..base.views_footer_link_group import get_footer_link_groups_active
from ...forms import forms as ff
from ...models import models as mf


class FooterLinkListView(ListView):
    template_name_v1 = "footer/admin/v1/footer_link/footer_link_list.html"
    template_name_v2 = "footer/admin/v2/footer_link/footer_link_list.html"
    model = mf.FooterLink
    filter_search_content_items = ListView.filter_search_content_items + [
        "link",
        "group__title",
    ]

    def get_queryset(self):
        query = super().get_queryset()
        req_get = self.request.GET
        open_newtab = (
            req_get.get("open_newtab") == "on" if req_get.get("open_newtab") else None
        )
        if open_newtab is not None:
            query = query.filter(open_in_newtab=open_newtab)
        return query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["groups"] = get_footer_link_groups_active().order_by(
            "-sort_order", "-datetime_create"
        )
        return context


class FooterLinkDetailView(DetailView):
    template_name_v1 = "footer/admin/v1/footer_link/footer_link_detail.html"
    template_name_v2 = "footer/admin/v2/footer_link/footer_link_detail.html"
    model = mf.FooterLink


class FooterLinkEditView(UpdateView):
    template_name_v1 = "footer/admin/v1/footer_link/footer_link_edit.html"
    template_name_v2 = "footer/admin/v2/footer_link/footer_link_edit.html"
    model = mf.FooterLink
    form_class = ff.FooterLinkForm
    my_success_url_v1 = "admin-v1-setting-footer-link-detail"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["groups"] = get_footer_link_groups_active().order_by(
            "-sort_order", "-datetime_create"
        )
        return context


class FooterLinkCreateView(CreateView):
    template_name_v1 = "footer/admin/v1/footer_link/footer_link_edit.html"
    template_name_v2 = "footer/admin/v2/footer_link/footer_link_edit.html"
    model = mf.FooterLink
    form_class = ff.FooterLinkForm
    my_success_url_v1 = "/panel-admin/setting/footer-link/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["groups"] = get_footer_link_groups_active().order_by(
            "-sort_order", "-datetime_create"
        )
        return context


class FooterLinkDeleteView(View):
    def post(self, request):
        pk = request.POST.get("pk")
        get_footer_link_with_pk(pk).delete()
        next_page = request.POST.get("next_page")
        if next_page[-6:] == "detail":
            return redirect(next_page, pk=pk)
        return redirect(next_page)
