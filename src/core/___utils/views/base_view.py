import re

from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse as _JsonResponse
from django.shortcuts import render as _render, redirect
from django.urls import reverse
from django.utils.functional import cached_property
from django.views.generic import (
    TemplateView as _TemplateView,
    ListView as _ListView,
    DetailView as _DetailView,
)
from django.views.generic.edit import (
    FormView as _FormView,
    CreateView as _CreateView,
    UpdateView as _UpdateView,
)

from ___utils.functions.string_function import print_debug
from ___utils.views.paginator_view import get_page_range, paginate_queryset
from __site_setting.views.base.views_base import site_setting_context
from __user.views.base.views_user import (
    get_user_with_email,
    get_user_with_phone,
)
from _locales import language_en, language_fa


def check_method_post(request):
    _is_method_post = False
    message = None
    if not request.method == "POST":
        message = "send_a_post_request_with_valid_parameter_only"
    else:
        _is_method_post = True
    return _is_method_post, message


def check_user_email_method_post(request):
    _email_exists = False
    usr = None
    _is_method_post, message = check_method_post(request)
    if not _is_method_post:
        message = message
    else:
        _is_method_post = True
        email = request.POST.get("email")

        # validation part
        if (not email or email is None) or (
            not re.match(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", email)
        ):
            _is_method_post = False
            message = "send_a_post_request_with_valid_parameter_only"
        else:
            user = get_user_with_email(email)
            if not user or user is None:
                message = "the_email_or_password_is_incorrect"
            else:
                _email_exists = True
                message = "email_already_exists"
                usr = user
    return _is_method_post, _email_exists, message, usr


def check_user_phone_method_post(request):
    _phone_exists = False
    usr = None
    _is_method_post, message = check_method_post(request)
    if not _is_method_post:
        message = message
    else:
        _is_method_post = True
        phone = request.POST.get("phone")

        # validation part
        if len(phone) < 10:
            _is_method_post = False
            message = "send_a_post_request_with_valid_parameter_only"
        else:
            user = get_user_with_phone(phone)
            if not user or user is None:
                message = "the_phone_or_password_is_incorrect"
            else:
                message = "phone_already_exists"
                usr = user
    return _is_method_post, _phone_exists, message, usr


def render(request, template_name, context=None):
    context = site_setting_context(context)
    context = set_dic_language_context(request.user_setting, context)
    return _render(request, template_name, context)


def JsonResponse(data, status=None, _function=None):
    print_debug(data, _function)
    return _JsonResponse(data, status=status)


def set_dic_language_context(user_setting, context=None):
    if context is None:
        context = {}
    context["dic_language"] = get_dic_language(user_setting)
    return context


def get_dic_language(user_setting=None):
    language = user_setting.get("language") if user_setting is not None else "en"
    dic = language_en if language == "en" else language_fa
    return dic


class TemplateView(_TemplateView):
    # template_name = '__TEMPLATE_NAME_PATH__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = site_setting_context(context)
        context = set_dic_language_context(self.request.user_setting, context)
        return context

    def get_version(self):
        try:
            req_path = self.request.path
            v_index = req_path.find("/v")
            if v_index != -1:
                return req_path[v_index + 1 : v_index + 3]
        except Exception as e:
            print(e)
        return "v1"

    def get_template_names(self):
        try:
            if self.get_version() == "v1":
                return self.template_name_v1
            else:
                return self.template_name_v2
        except Exception as e:
            print(e)
            return self.template_name


class DetailView(_DetailView):
    # template_name = '__TEMPLATE_NAME_PATH__'
    # model = __MODEL_NAME__
    context_object_name = "object"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = site_setting_context(context)
        context = set_dic_language_context(self.request.user_setting, context)
        if hasattr(self.object, "get_history_logs"):
            context["has_log"] = True
            logs = self.object.get_history_logs()
            page_log = self.request.GET.get("page")
            paginate_queryset(context, logs, page_log, reverse=True)
        return context

    def get_version(self):
        try:
            req_path = self.request.path
            v_index = req_path.find("/v")
            if v_index != -1:
                return req_path[v_index + 1 : v_index + 3]
        except Exception as e:
            print(e)
        return "v1"

    def get_template_names(self):
        try:
            if self.get_version() == "v1":
                return self.template_name_v1
            else:
                return self.template_name_v2
        except Exception as e:
            print(e)
            return self.template_name


class ListView(_ListView):
    context_object_name = "object_list"
    ordering = ["-sort_order", "-datetime_create"]
    paginate_by = 10
    filter_search_content_items = ["title", "description", "pk"]

    def model_has_field(self, field_name: str) -> bool:
        return field_name in {f.name for f in self.model._meta.get_fields()}

    @cached_property
    def cached_queryset(self):
        return super().get_queryset()

    @staticmethod
    def normalize_datetime_range(req_get, param_name, field_prefix):
        rng = req_get.get(param_name)
        if not rng:
            return None
        try:
            if rng.find(" to "):
                date_start, date_end = [
                    x.strip().replace("/", "-") for x in rng.split(" to ")
                ]
            else:
                date_start, date_end = [
                    x.strip().replace("/", "-") for x in rng.split(" - ")
                ]
        except ValueError:
            return None
        return {
            f"{field_prefix}__gte": date_start,
            f"{field_prefix}__lte": date_end,
        }

    def get_queryset(self):
        query = self.cached_queryset
        req_get = self.request.GET

        content = req_get.get("q").strip() if req_get.get("q") else None
        if content:
            query_filter = Q()
            for item in self.filter_search_content_items:
                if self.model_has_field(item):
                    query_filter |= Q(**{f"{item}__icontains": content})
            if query_filter:
                query = query.filter(query_filter)

        if self.model_has_field("is_active"):
            status = req_get.get("status") == "on" if req_get.get("status") else None
            if status is not None:
                query = query.filter(is_active=status)

        if self.model_has_field("is_deleted"):
            deleted = req_get.get("deleted") == "on" if req_get.get("deleted") else None
            query = (
                query.filter(is_deleted=deleted)
                if deleted is not None
                else query.filter(is_deleted=False)
            )

        dr_create = self.normalize_datetime_range(
            req_get, "date_range_create", "datetime_create"
        )
        if dr_create and self.model_has_field("datetime_create"):
            query = query.filter(**dr_create)

        dr_update = self.normalize_datetime_range(
            req_get, "date_range_update", "datetime_update"
        )
        if dr_update and self.model_has_field("datetime_update"):
            query = query.filter(**dr_update)

        dr_delete = self.normalize_datetime_range(
            req_get, "date_range_delete", "datetime_delete"
        )
        if dr_delete and self.model_has_field("datetime_delete"):
            query = query.filter(**dr_delete)

        return query

    # @staticmethod
    # def set_filter_query(request, context):
    #     filtered_params = {
    #         k: v for k, v in request.GET.items() if v and v[0] and k != "page"
    #     }
    #     filter_query = urlencode(filtered_params)
    #     if filter_query:
    #         context["filter_query"] = f"?{filter_query}&"
    #     return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_range"] = get_page_range(
            current_page=context["page_obj"].number,
            total_page=context["paginator"].num_pages,
        )
        context = site_setting_context(context)
        context = set_dic_language_context(self.request.user_setting, context)
        return context

    def get_ordering(self):
        default_ordering = self.ordering
        valid_ordering = []
        if default_ordering:
            for field_name in default_ordering:
                actual_field_name = field_name.lstrip("-")
                if self.model_has_field(actual_field_name):
                    valid_ordering.append(field_name)
        return valid_ordering or None

    def get_paginate_by(self, queryset, **kwargs):
        return self.request.GET.get("page_size", self.paginate_by)

    def get_version(self):
        try:
            req_path = self.request.path
            v_index = req_path.find("/v")
            if v_index != -1:
                return req_path[v_index + 1 : v_index + 3]
        except Exception as e:
            print(e)
        return "v1"

    def get_template_names(self):
        try:
            if self.get_version() == "v1":
                return self.template_name_v1
            else:
                return self.template_name_v2
        except Exception as e:
            print(e)
            return self.template_name


class FormView(_FormView):
    # template_name = '__TEMPLATE_NAME_PATH__'
    # form_class = __FORM_MODEL__
    # success_url = '__SUCCESS_ROUTE_PATH__'
    #
    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs.update({'some_extra_kwarg': 'my_data'})
    #     return kwargs

    # def form_valid(self, form):
    #     return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = site_setting_context(context)
        context = set_dic_language_context(self.request.user_setting, context)
        return context

    def get_version(self):
        try:
            req_path = self.request.path
            v_index = req_path.find("/v")
            if v_index != -1:
                return req_path[v_index + 1 : v_index + 3]
        except Exception as e:
            print(e)
        return "v1"

    def get_template_names(self):
        try:
            if self.get_version() == "v1":
                return self.template_name_v1
            else:
                return self.template_name_v2
        except Exception as e:
            print(e)
            return self.template_name


class UpdateView(_UpdateView):
    # template_name = '__TEMPLATE_NAME_PATH__'
    # model = __MODEL_NAME__
    # form_class = __FORM_MODEL__
    # success_url = '__SUCCESS_ROUTE_PATH__'
    my_success_url_v1 = None

    # ############# is Not Important ############# #
    # def form_valid(self, form):
    #     return super().form_valid(form)

    def get_version(self):
        try:
            req_path = self.request.path
            v_index = req_path.find("/v")
            if v_index != -1:
                return req_path[v_index + 1 : v_index + 3]
        except Exception as e:
            print(e)
        return "v1"

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, error)

        return redirect(self.request.META.get("HTTP_REFERER"))

    def get_success_url(self):
        pk = self.kwargs.get("pk")
        if pk is None:
            pk = self.kwargs.get("slug")
        _success_url = (
            self.my_success_url_v1
            if self.get_version() == "v1"
            else self.my_success_url_v2
        )
        _success_url = self.success_url if _success_url is None else _success_url
        return reverse(_success_url, kwargs={"pk": pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = site_setting_context(context)
        context = set_dic_language_context(self.request.user_setting, context)
        return context

    def get_template_names(self):
        try:
            if self.get_version() == "v1":
                return self.template_name_v1
            else:
                return self.template_name_v2
        except Exception as e:
            print(e)
            return self.template_name


class CreateView(_CreateView):
    # template_name = '__TEMPLATE_NAME_PATH__'
    # model = __MODEL_NAME__
    # fields = '__all__'
    # success_url = '__SUCCESS_ROUTE_PATH__'
    my_success_url_v1 = None

    # ############# is Not Important ############# #
    # def form_valid(self, form):
    #     return super().form_valid(form)

    def get_version(self):
        try:
            req_path = self.request.path
            v_index = req_path.find("/v")
            if v_index != -1:
                return req_path[v_index + 1 : v_index + 3]
        except Exception as e:
            print(e)
        return "v1"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = site_setting_context(context)
        context = set_dic_language_context(self.request.user_setting, context)
        return context

    def get_success_url(self):
        _success_url = (
            self.my_success_url_v1
            if self.get_version() == "v1"
            else self.my_success_url_v2
        )
        _success_url = self.success_url if _success_url is None else _success_url

        try:
            if "_addanother" in self.request.POST:
                return reverse(_success_url + "-add")
            elif "_save_draft" in self.request.POST:
                obj_pk = self.get_form().instance.pk
                return reverse(_success_url + "-detail", kwargs={"pk": obj_pk})
            else:
                return reverse(_success_url + "-list")
        except Exception as e:
            print(e)
            return reverse(_success_url)

    def get_template_names(self):
        try:
            if self.get_version() == "v1":
                return self.template_name_v1
            else:
                return self.template_name_v2
        except Exception as e:
            print(e)
            return self.template_name
