from django.shortcuts import redirect
from django.views.generic import View

from _0_utils.views.base_view import (
    ListView,
    DetailView,
    UpdateView,
    CreateView,
)
from ..base.views import get_category_with_pk
from ...forms import forms as ff
from ...models import models as mm


class CategoryListView(ListView):
    template_name_v1 = "category/admin/v1/category_list.html"
    template_name_v2 = "category/admin/v2/category_list.html"
    model = mm.Category
    filter_search_content_items = ListView.filter_search_content_items + ["slug"]
    ordering = ["-sort_order"]


class CategoryDetailView(DetailView):
    template_name_v1 = "category/admin/v1/category_detail.html"
    template_name_v2 = "category/admin/v2/category_detail.html"
    model = mm.Category


class CategoryEditView(UpdateView):
    template_name_v1 = "category/admin/v1/category_edit.html"
    template_name_v2 = "category/admin/v2/category_edit.html"
    model = mm.Category
    form_class = ff.CategoryForm
    my_success_url_v1 = "admin-v1-category:detail"
    my_success_url_v2 = "admin-v2-category:detail"

    def form_valid(self, form):
        clear_image = form.cleaned_data.get("clear_image")
        if clear_image:
            self.object.image = None
        return super().form_valid(form)


class CategoryCreateView(CreateView):
    template_name_v1 = "category/admin/v1/category_edit.html"
    template_name_v2 = "category/admin/v2/category_edit.html"
    model = mm.Category
    form_class = ff.CategoryForm
    my_success_url_v1 = "admin-v1-category"
    my_success_url_v2 = "admin-v2-category"


class CategoryDeleteView(View):
    def post(self, request):
        pk = request.POST.get("pk")
        get_category_with_pk(pk).delete()
        next_page = request.POST.get("next_page")
        if next_page[-6:] == "detail":
            return redirect(next_page, pk=pk)
        return redirect(next_page)
