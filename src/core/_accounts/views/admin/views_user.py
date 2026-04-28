from django.db.models import Q
from django.shortcuts import redirect
from django.views.generic import View

from ___utils.views.base_view import ListView, DetailView, UpdateView
from ..base.views_user import get_user_gender_choices, get_user_with_code
from ..._modules.register_user.models.models import RegisterUser
from ..._modules.register_user.views.base.views import (
    get_register_user_with_id,
)
from ...forms import forms_user as fu
from ...models import User


class AdminListView(ListView):
    template_name_v1 = "__user/admin/v1/user/has_wallet/user_list.html"
    template_name_v2 = "__user/admin/v2/user/has_wallet/user_list.html"
    model = User
    ordering = ["-date_joined", "-id"]

    def get_queryset(self):
        query = super().get_queryset()
        query = query.filter(is_staff=True)
        req_get = self.request.GET
        content = req_get.get("content").strip() if req_get.get("content") else None
        if content:
            query = query.filter(
                Q(first_name__contains=content)
                | Q(last_name__contains=content)
                | Q(email__contains=content)
                | Q(username__contains=content)
            )

        return query


class CustomerListView(ListView):
    template_name_v1 = "__user/admin/v1/user/has_wallet/user_list.html"
    template_name_v2 = "__user/admin/v2/user/has_wallet/user_list.html"
    model = User
    ordering = ["-date_joined", "-id"]

    def get_queryset(self):
        query = super().get_queryset()
        query = query.filter(is_staff=False)
        req_get = self.request.GET
        content = req_get.get("content").strip() if req_get.get("content") else None
        if content:
            query = query.filter(
                Q(first_name__contains=content)
                | Q(last_name__contains=content)
                | Q(email__contains=content)
                | Q(username__contains=content)
            )

        return query


class RegisterListView(ListView):
    template_name_v1 = "register_user/admin/v1/register_list.html"
    template_name_v2 = "register_user/admin/v2/register_list.html"
    model = RegisterUser
    ordering = ["-datetime", "email"]

    def get_queryset(self):
        query = super().get_queryset()
        req_get = self.request.GET
        content = req_get.get("content").strip() if req_get.get("content") else None
        if content:
            query = query.filter(
                Q(first_name__contains=content)
                | Q(last_name__contains=content)
                | Q(email__contains=content)
                | Q(activation_code__contains=content)
            )

        return query


class RegisterDeleteView(View):
    def post(self, request):
        _id = request.POST.get("slug")
        get_register_user_with_id(_id).delete()
        next_page = request.POST.get("next_page")
        if next_page[-6:] == "detail":
            return redirect(next_page, slug=_id)
        return redirect(next_page)


class UserDetailView(DetailView):
    template_name_v1 = "__user/admin/v1/user/has_wallet/user_detail.html"
    template_name_v2 = "__user/admin/v2/user/has_wallet/user_detail.html"
    model = User
    slug_field = "code"


class UserEditView(UpdateView):
    template_name_v1 = "__user/admin/v1/user/has_wallet/user_edit.html"
    template_name_v2 = "__user/admin/v2/user/has_wallet/user_edit.html"
    model = User
    form_class = fu.UserForm
    slug_field = "code"
    my_success_url_v1 = "admin-v1-user-detail"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["genders"] = get_user_gender_choices()
        return context

    def form_valid(self, form):
        clear_avatar = form.cleaned_data.get("clear_avatar")
        if clear_avatar:
            self.object.avatar = None
        return super().form_valid(form)


class UserDeleteView(View):
    def post(self, request):
        code = request.POST.get("code")
        get_user_with_code(code).delete()
        next_page = request.POST.get("next_page")
        if next_page[-6:] == "detail":
            return redirect(next_page, slug=code)
        return redirect(next_page)


class ToggleStaffView(View):
    def post(self, request):
        code = request.POST.get("code")
        user = get_user_with_code(code)
        if user:
            user.is_staff = not user.is_staff
            user.save()
        return redirect("admin-v1-user-detail", slug=code)


class ToggleActiveView(View):
    def post(self, request):
        code = request.POST.get("code")
        user = get_user_with_code(code)
        if user:
            user.is_active = not user.is_active
            user.save()
        return redirect("admin-v1-user-detail", slug=code)


class ToggleBanView(View):
    def post(self, request):
        code = request.POST.get("code")
        user = get_user_with_code(code)
        if user:
            user.is_ban = not user.is_ban
            user.save()
        return redirect("admin-v1-user-detail", slug=code)
