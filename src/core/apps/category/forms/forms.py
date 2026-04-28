from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget

from ..models import models as mm


class CategoryForm(forms.ModelForm):
    clear_image = forms.BooleanField(
        required=False, widget=forms.CheckboxInput(attrs={"class": "form-check-input"})
    )

    class Meta:
        model = mm.Category
        exclude = [
            "slug",
            "is_deleted",
            "datetime_create",
            "datetime_update",
            "datetime_delete",
        ]
        widgets = {
            "title_en": forms.TextInput(
                attrs={
                    "class": "form-control fs-5",
                    "placeholder": "Title",
                    "required": True,
                }
            ),
            "title_fa": forms.TextInput(
                attrs={
                    "class": "form-control fs-5",
                    "placeholder": "Title",
                    "required": True,
                }
            ),
            "sort_order": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Sort Order"}
            ),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "alt_image_name": forms.TextInput(
                attrs={"class": "form-control fs-5", "placeholder": "Alt Image Name"}
            ),
            "image": forms.FileInput(
                attrs={"class": "form-control form-control-sm", "required": False}
            ),
            "description_en": CKEditor5Widget(),
            "description_fa": CKEditor5Widget(),
        }
        error_messages = {
            "title_en": {
                "required": "Title is required",
            },
            "title_fa": {
                "required": "Title is required",
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields["title_en"].widget.attrs.update({"class": "form-control fs-5"})
        self.fields["title_en"].widget.attrs["class"] = "form-control fs-5"
