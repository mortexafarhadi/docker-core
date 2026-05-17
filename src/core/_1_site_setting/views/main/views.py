from django.http import HttpResponse
from django.views.decorators.cache import cache_page
from time import sleep

from _0_utils.service.email_service import send_mail
from _0_utils.views.base_view import TemplateView
from _0_utils.views.base_view import render
from ..._modules.footer.views.base.views_footer_link_group import (
    get_footer_link_groups_active_prefetch_footer_link,
)
from ..._modules.header.views.base.views_header_link_group import (
    get_header_link_groups_active_prefetch_header_link,
)
from ...tasks import celery_task


class IndexView(TemplateView):
    template_name = "_1_site_setting/main/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header_groups"] = get_header_link_groups_active_prefetch_header_link()
        context["footer_groups"] = get_footer_link_groups_active_prefetch_footer_link()
        return context


def test_celery(request):
    celery_task.delay()
    return HttpResponse("<h1>Done Test Celery</h1>")


# @cache_page(60 * 1)
@cache_page(10)
def test_cache(request):
    sleep(1)
    return render(request, "_1_site_setting/main/test.html")


def test_mail(request):
    send_mail(
        "Test Mail Subject", "to@example.com", {"test": "test"}, "emails/test.html"
    )
    return HttpResponse("<h1>Test Mail Done</h1>")
