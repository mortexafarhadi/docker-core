from django.shortcuts import redirect
from django.views.generic import View

from _0_utils.views.base_view import (
    ListView,
    DetailView,
    UpdateView,
    CreateView,
)
from ..base.views_site import get_site_setting_with_pk
from ...forms import forms as fs
from ...models import models as ms


class SiteSettingListView(ListView):
    template_name_v1 = "_1_site_setting/admin/v1/site/site_list.html"
    template_name_v2 = "_1_site_setting/admin/v2/site/site_list.html"
    model = ms.SiteSetting
    filter_search_content_items = [
        "site_name",
        "link",
        "email",
        "phone",
        "fax",
        "address",
        "footer_description",
        "copyright_main_text_1",
        "copyright_main_text_2",
        "copyright_auth_text_1",
        "copyright_auth_text_2",
        "copyright_panels_text_1",
        "copyright_panels_text_2",
        "slug",
        "description",
    ]

    def get_queryset(self):
        query = super().get_queryset()
        req_get = self.request.GET

        main = req_get.get("main") == "on" if req_get.get("main") else None
        if main is not None:
            query = query.filter(is_main=main)

        return query


class SiteSettingDetailView(DetailView):
    template_name_v1 = "_1_site_setting/admin/v1/site/site_detail.html"
    template_name_v2 = "_1_site_setting/admin/v2/site/site_detail.html"
    model = ms.SiteSetting


class SiteSettingEditView(UpdateView):
    template_name_v1 = "_1_site_setting/admin/v1/site/site_edit.html"
    template_name_v2 = "_1_site_setting/admin/v2/site/site_edit.html"
    model = ms.SiteSetting
    form_class = fs.SiteSettingForm
    my_success_url_v1 = "admin-v1-setting-site:detail"

    def form_valid(self, form):
        clear_logo_header = form.cleaned_data.get("clear_logo_header")
        if clear_logo_header:
            self.object.logo_header = None
        clear_logo_footer = form.cleaned_data.get("clear_logo_footer")
        if clear_logo_footer:
            self.object.logo_footer = None
        clear_section_head_favicon = form.cleaned_data.get("clear_section_head_favicon")
        if clear_section_head_favicon:
            self.object.section_head_favicon = None
        clear_logo_preload = form.cleaned_data.get("clear_logo_preload")
        if clear_logo_preload:
            self.object.logo_preload = None
        return super().form_valid(form)


class SiteSettingCreateView(CreateView):
    template_name_v1 = "_1_site_setting/admin/v1/site/site_edit.html"
    template_name_v2 = "_1_site_setting/admin/v2/site/site_edit.html"
    model = ms.SiteSetting
    form_class = fs.SiteSettingForm
    my_success_url_v1 = "/panel-admin/setting/site/"


class SiteSettingDeleteView(View):
    def post(self, request):
        pk = request.POST.get("pk")
        get_site_setting_with_pk(pk).delete()
        next_page = request.POST.get("next_page")
        if next_page[-6:] == "detail":
            return redirect(next_page, pk=pk)
        return redirect(next_page)
