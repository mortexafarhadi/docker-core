from django.shortcuts import redirect
from django.views.generic import View

from _0_utils.views.base_view import (
    ListView,
    DetailView,
    UpdateView,
    CreateView,
)
from ..base.views_header_link import get_header_link_with_pk
from ..base.views_header_link_group import get_header_link_groups_active
from ...forms import forms as fh
from ...models import models as mh


class HeaderLinkListView(ListView):
    template_name_v1 = "header/admin/v1/header_link/header_link_list.html"
    template_name_v2 = "header/admin/v2/header_link/header_link_list.html"
    model = mh.HeaderLink
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

        group = req_get.get("group").strip() if req_get.get("group") else None
        if group is not None:
            query = query.filter(group__id=group)

        return query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["groups"] = get_header_link_groups_active().order_by(
            "-sort_order", "-datetime_create"
        )
        return context


class HeaderLinkDetailView(DetailView):
    template_name_v1 = "header/admin/v1/header_link/header_link_detail.html"
    template_name_v2 = "header/admin/v2/header_link/header_link_detail.html"
    model = mh.HeaderLink


class HeaderLinkEditView(UpdateView):
    template_name_v1 = "header/admin/v1/header_link/header_link_edit.html"
    template_name_v2 = "header/admin/v2/header_link/header_link_edit.html"
    model = mh.HeaderLink
    form_class = fh.HeaderLinkForm
    my_success_url_v1 = "admin-v1-setting-header-link-detail"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["groups"] = get_header_link_groups_active().order_by(
            "-sort_order", "-datetime_create"
        )
        return context


class HeaderLinkCreateView(CreateView):
    template_name_v1 = "header/admin/v1/header_link/header_link_edit.html"
    template_name_v2 = "header/admin/v2/header_link/header_link_edit.html"
    model = mh.HeaderLink
    form_class = fh.HeaderLinkForm
    my_success_url_v1 = "/panel-admin/setting/header-link/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["groups"] = get_header_link_groups_active().order_by(
            "-sort_order", "-datetime_create"
        )

        return context


class HeaderLinkDeleteView(View):
    def post(self, request):
        pk = request.POST.get("pk")
        get_header_link_with_pk(pk).delete()
        next_page = request.POST.get("next_page")
        if next_page[-6:] == "detail":
            return redirect(next_page, pk=pk)
        return redirect(next_page)
