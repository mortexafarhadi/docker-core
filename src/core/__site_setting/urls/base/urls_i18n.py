from django.urls import path

from __site_setting.views.main import views as vv

app_name = "main"

urlpatterns = [
    path("test-celery/", vv.test_celery, name="test-celery"),
    path("test-cache/", vv.test_cache, name="test-cache"),
    path("test-mail/", vv.test_mail, name="test-mail"),
    path("", vv.IndexView.as_view(), name="index"),
]
