from django.urls import path
from . import views as vv

urlpatterns = [
    path("site-setting/<int:count>", vv.fake_site_setting, name="fake-site-setting"),
]
