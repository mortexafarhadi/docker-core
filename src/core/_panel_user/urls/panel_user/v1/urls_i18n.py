from django.urls import path

from ....views.panel_user import views as vv

app_name = "user-v1"

urlpatterns = [
    path("dashboard/", vv.DashboardView.as_view(), name="dashboard"),
]
