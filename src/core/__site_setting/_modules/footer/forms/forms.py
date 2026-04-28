from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget

from ..models import models as mf
from ..views.base.views_footer_link_group import get_footer_link_groups_active


class FooterLinkGroupForm(forms.ModelForm):
    class Meta:
        model = mf.FooterLinkGroup
        exclude = [
            "is_deleted",
            "datetime_create",
            "datetime_update",
            "datetime_delete",
        ]
        widgets = {
            "site_type": forms.Select(attrs={"class": "form-select"}),
            "title": forms.TextInput(
                attrs={"class": "form-control fs-5", "required": True}
            ),
            "sort_order": forms.NumberInput(attrs={"class": "form-control"}),
            "link": forms.URLInput(attrs={"class": "form-control", "required": False}),
            "open_in_newtab": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "has_child": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "is_move_mode": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "move_target_id": forms.TextInput(
                attrs={"class": "form-control fs-5", "required": False}
            ),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "description": CKEditor5Widget(),
        }


class FooterLinkForm(forms.ModelForm):
    group = forms.ModelChoiceField(
        queryset=get_footer_link_groups_active().order_by(
            "-sort_order", "-datetime_create"
        ),
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    class Meta:
        model = mf.FooterLink
        exclude = [
            "is_deleted",
            "datetime_create",
            "datetime_update",
            "datetime_delete",
        ]
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control fs-5", "required": True}
            ),
            "link": forms.URLInput(attrs={"class": "form-control", "required": True}),
            "sort_order": forms.NumberInput(attrs={"class": "form-control"}),
            "open_in_newtab": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "description": CKEditor5Widget(),
        }
