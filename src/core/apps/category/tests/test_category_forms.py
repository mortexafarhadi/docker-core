from apps.category.forms.forms import CategoryForm


class TestCategoryForms:
    def test_category_form_no_data(self):
        form = CategoryForm(data={})
        assert not form.is_valid()

    def test_category_form_valid_data(self):
        form = CategoryForm(
            data={
                "title_en": "Test",
                "title_fa": "تست",
                "sort_order": 12,
                "is_active": True,
                "alt_image_name": "alt name",
                "description_en": "description",
                "description_fa": "توضیحات",
            }
        )
        assert form.is_valid()
