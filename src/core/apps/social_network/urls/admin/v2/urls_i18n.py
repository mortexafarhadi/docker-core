from django.urls import path

from ....views.admin import views as vv

app_name = "admin-v2-social-network"

urlpatterns = [
    path("add/", vv.SocialNetworkCreateView.as_view(), name="add"),
    path("delete/", vv.SocialNetworkDeleteView.as_view(), name="delete"),
    path("edit/<pk>/", vv.SocialNetworkEditView.as_view(), name="edit"),
    path("<pk>/", vv.SocialNetworkDetailView.as_view(), name="detail"),
    path("", vv.SocialNetworkListView.as_view(), name="list"),
]
