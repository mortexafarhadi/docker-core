from django.urls import path, re_path

from ....views.admin import views as vv

app_name = "admin-v1-category"

urlpatterns = [
    path("add/", vv.CategoryCreateView.as_view(), name="add"),
    path("delete/", vv.CategoryDeleteView.as_view(), name="delete"),
    path("edit/<pk>/", vv.CategoryEditView.as_view(), name="edit"),
    path("<pk>/", vv.CategoryDetailView.as_view(), name="detail"),
    path("", vv.CategoryListView.as_view(), name="list"),
    # # with regex persian slug
    re_path(r"(?P<slug>[-\w]+)/", vv.CategoryDetailView.as_view(), name="detail"),
]
