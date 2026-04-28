from django.urls import reverse, resolve

from apps.category.views.admin import views as vv


class TestCategoryUrlV1:
    def test_v1_category_list_resolve(self):
        url = reverse("admin-v1-category:list")
        assert resolve(url).func.view_class == vv.CategoryListView

    def test_v1_category_add_resolve(self):
        url = reverse("admin-v1-category:add")
        assert resolve(url).func.view_class == vv.CategoryCreateView

    def test_v1_category_delete_resolve(self):
        url = reverse("admin-v1-category:delete")
        assert resolve(url).func.view_class == vv.CategoryDeleteView

    def test_v1_category_detail_resolve(self):
        url = reverse("admin-v1-category:detail", kwargs={"pk": 1})
        assert resolve(url).func.view_class == vv.CategoryDetailView

    def test_v1_category_edit_resolve(self):
        url = reverse("admin-v1-category:edit", kwargs={"pk": 1})
        assert resolve(url).func.view_class == vv.CategoryEditView
