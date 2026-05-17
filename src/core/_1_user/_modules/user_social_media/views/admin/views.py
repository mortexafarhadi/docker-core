from django.shortcuts import redirect
from django.views.generic import View

from _0_utils.views.base_view import (
    ListView,
    DetailView,
    UpdateView,
    CreateView,
)
from ..base.views import get_user_social_media_with_id
from ...forms.forms import UserSocialMediaForm
from ...models.models import UserSocialMedia
from _1_user.views.base.views_user import get_users_all
from apps.social_network.views.base.views import get_social_networks_all


class UserSocialMediaListView(ListView):
    template_name_v1 = "user_social_media/admin/v1/social_media_list.html"
    template_name_v2 = "user_social_media/admin/v2/social_media_list.html"
    model = UserSocialMedia
    filter_search_content_items = ListView.filter_search_content_items + [
        "link",
        "group__title",
    ]


class UserSocialMediaDetailView(DetailView):
    template_name_v1 = "user_social_media/admin/v1/social_media_detail.html"
    template_name_v2 = "user_social_media/admin/v2/social_media_detail.html"
    model = UserSocialMedia


class UserSocialMediaEditView(UpdateView):
    template_name_v1 = "user_social_media/admin/v1/social_media_edit.html"
    template_name_v2 = "user_social_media/admin/v2/social_media_edit.html"
    model = UserSocialMedia
    form_class = UserSocialMediaForm
    my_success_url_v1 = "admin-v1-user-social-media-detail"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["users"] = get_users_all().order_by("-date_joined")
        context["social_networks"] = get_social_networks_all().order_by(
            "-datetime_create"
        )
        return context


class UserSocialMediaCreateView(CreateView):
    template_name_v1 = "user_social_media/admin/v1/social_media_edit.html"
    template_name_v2 = "user_social_media/admin/v2/social_media_edit.html"
    model = UserSocialMedia
    form_class = UserSocialMediaForm
    my_success_url_v1 = "/panel-admin/setting/footer-link/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["users"] = get_users_all().order_by("-date_joined")
        context["social_networks"] = get_social_networks_all().order_by(
            "-datetime_create"
        )
        return context


class UserSocialMediaDeleteView(View):
    def post(self, request):
        pk = request.POST.get("pk")
        get_user_social_media_with_id(pk).delete()
        next_page = request.POST.get("next_page")
        if next_page[-6:] == "detail":
            return redirect(next_page, pk=pk)
        return redirect(next_page)
