from django.urls import path

from ..views import views as vv

app_name = "base"

urlpatterns = [
    path("change-language/", vv.ChangeLanguageView.as_view(), name="change-language"),
    path(
        "toggle-dark-mode/",
        vv.ToggleDarkModeStatusView.as_view(),
        name="toggle-dark-mode",
    ),
    path(
        "change-background-mode/",
        vv.ChangeBackgroundModeView.as_view(),
        name="change-background-mode",
    ),
    path(
        "change-color-mode/", vv.ChangeColorModeView.as_view(), name="change-color-mode"
    ),
    path(
        "change-sidebar-mode/",
        vv.ChangeSidebarModeView.as_view(),
        name="change-sidebar-mode",
    ),
]
