from django.shortcuts import redirect
from django.views.generic import View

from _0_utils.views.base_view import (
    ListView,
    DetailView,
    UpdateView,
    CreateView,
)
from ..base.views_header_link_group import get_header_link_group_with_pk
from ...forms import forms as fh
from ...models import models as mh


class HeaderLinkGroupListView(ListView):
    template_name_v1 = "header/admin/v1/header_link_group/header_link_group_list.html"
    template_name_v2 = "header/admin/v2/header_link_group/header_link_group_list.html"
    model = mh.HeaderLinkGroup
    filter_search_content_items = ListView.filter_search_content_items + [
        "link",
        "move_target_id",
    ]

    def get_queryset(self):
        query = super().get_queryset()
        req_get = self.request.GET

        has_child = (
            req_get.get("has_child") == "on" if req_get.get("has_child") else None
        )
        if has_child is not None:
            query = query.filter(has_child=has_child)

        move_mode = (
            req_get.get("move_mode") == "on" if req_get.get("move_mode") else None
        )
        if move_mode is not None:
            query = query.filter(is_move_mode=move_mode)

        open_newtab = (
            req_get.get("open_newtab") == "on" if req_get.get("open_newtab") else None
        )
        if open_newtab is not None:
            query = query.filter(open_in_newtab=open_newtab)

        return query


class HeaderLinkGroupDetailView(DetailView):
    template_name_v1 = "header/admin/v1/header_link_group/header_link_group_detail.html"
    template_name_v2 = "header/admin/v2/header_link_group/header_link_group_detail.html"
    model = mh.HeaderLinkGroup


class HeaderLinkGroupEditView(UpdateView):
    template_name_v1 = "header/admin/v1/header_link_group/header_link_group_edit.html"
    template_name_v2 = "header/admin/v2/header_link_group/header_link_group_edit.html"
    model = mh.HeaderLinkGroup
    form_class = fh.HeaderLinkGroupForm
    my_success_url_v1 = "admin-v1-setting-header-group-detail"


class HeaderLinkGroupCreateView(CreateView):
    template_name_v1 = "header/admin/v1/header_link_group/header_link_group_edit.html"
    template_name_v2 = "header/admin/v2/header_link_group/header_link_group_edit.html"
    model = mh.HeaderLinkGroup
    form_class = fh.HeaderLinkGroupForm
    my_success_url_v1 = "/panel-admin/setting/header-group/"


class HeaderLinkGroupDeleteView(View):
    def post(self, request):
        pk = request.POST.get("pk")
        get_header_link_group_with_pk(pk).delete()
        next_page = request.POST.get("next_page")
        if next_page[-6:] == "detail":
            return redirect(next_page, pk=pk)
        return redirect(next_page)
