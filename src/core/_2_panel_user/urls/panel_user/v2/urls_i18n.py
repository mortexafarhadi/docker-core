from django.urls import path

from ....views.panel_user import views as vv

app_name = "user-v2"

urlpatterns = [
    path("dashboard/", vv.DashboardView.as_view(), name="dashboard"),
]
