from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget

from __site_setting.models import models as ms


class SiteSettingForm(forms.ModelForm):
    clear_logo_header = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )
    clear_logo_footer = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )
    clear_logo_preload = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )
    clear_section_head_favicon = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )

    class Meta:
        model = ms.SiteSetting
        exclude = [
            "is_deleted",
            "datetime_create",
            "datetime_update",
            "datetime_delete",
        ]
        widgets = {
            "site_type": forms.Select(attrs={"class": "form-select"}),
            "section_head_title": forms.TextInput(
                attrs={"class": "form-control fs-5", "required": True}
            ),
            "section_head_html_language": forms.TextInput(
                attrs={"class": "form-control fs-5", "required": True}
            ),
            "section_head_description": forms.Textarea(
                attrs={
                    "class": "form-control h-auto fs-4",
                    "rows": 6,
                    "required": False,
                }
            ),
            "section_head_keywords": forms.Textarea(
                attrs={
                    "class": "form-control h-auto fs-4",
                    "rows": 6,
                    "required": False,
                }
            ),
            "section_head_author": forms.Textarea(
                attrs={
                    "class": "form-control h-auto fs-4",
                    "rows": 6,
                    "required": False,
                }
            ),
            "section_head_favicon": forms.FileInput(
                attrs={
                    "class": "form-control form-control-lg",
                    "required": False,
                }
            ),
            "site_name": forms.TextInput(
                attrs={"class": "form-control fs-5", "required": True}
            ),
            "link": forms.URLInput(attrs={"class": "form-control", "required": False}),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "required": False}
            ),
            "phone": forms.TextInput(
                attrs={"class": "form-control fs-5", "required": False}
            ),
            "fax": forms.TextInput(
                attrs={"class": "form-control fs-5", "required": False}
            ),
            "address": forms.Textarea(
                attrs={
                    "class": "form-control h-auto fs-4",
                    "rows": 6,
                    "required": False,
                }
            ),
            "logo_header": forms.FileInput(
                attrs={
                    "class": "form-control form-control-lg",
                    "required": False,
                }
            ),
            "logo_footer": forms.FileInput(
                attrs={
                    "class": "form-control form-control-lg",
                    "required": False,
                }
            ),
            "logo_preload": forms.FileInput(
                attrs={
                    "class": "form-control form-control-lg",
                    "required": False,
                }
            ),
            "verify_code_digits": forms.NumberInput(
                attrs={"class": "form-control", "required": False}
            ),
            "thumbnail_quality": forms.NumberInput(
                attrs={"class": "form-control", "required": False}
            ),
            "thumbnail_size": forms.TextInput(
                attrs={"class": "form-control fs-5", "required": False}
            ),
            "footer_description": forms.Textarea(
                attrs={
                    "class": "form-control h-auto fs-4",
                    "rows": 6,
                    "required": False,
                }
            ),
            "footer_link_1_active": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
            "footer_link_1_text": forms.TextInput(
                attrs={"class": "form-control fs-5", "required": True}
            ),
            "footer_link_1_url": forms.URLInput(
                attrs={"class": "form-control", "required": False}
            ),
            "footer_link_2_active": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
            "footer_link_2_text": forms.TextInput(
                attrs={"class": "form-control fs-5", "required": True}
            ),
            "footer_link_2_url": forms.URLInput(
                attrs={"class": "form-control", "required": False}
            ),
            "footer_link_3_active": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
            "footer_link_3_text": forms.TextInput(
                attrs={"class": "form-control fs-5", "required": True}
            ),
            "footer_link_3_url": forms.URLInput(
                attrs={"class": "form-control", "required": False}
            ),
            "copyright_main_text_1": forms.Textarea(
                attrs={
                    "class": "form-control h-auto fs-4",
                    "rows": 6,
                    "required": False,
                }
            ),
            "copyright_main_text_2": forms.Textarea(
                attrs={
                    "class": "form-control h-auto fs-4",
                    "rows": 6,
                    "required": False,
                }
            ),
            "copyright_main_link_text": forms.TextInput(
                attrs={"class": "form-control fs-5", "required": True}
            ),
            "copyright_main_link_url": forms.URLInput(
                attrs={"class": "form-control", "required": False}
            ),
            "copyright_auth_text_1": forms.Textarea(
                attrs={
                    "class": "form-control h-auto fs-4",
                    "rows": 6,
                    "required": False,
                }
            ),
            "copyright_auth_text_2": forms.Textarea(
                attrs={
                    "class": "form-control h-auto fs-4",
                    "rows": 6,
                    "required": False,
                }
            ),
            "copyright_auth_link_text": forms.TextInput(
                attrs={"class": "form-control fs-5", "required": True}
            ),
            "copyright_auth_link_url": forms.URLInput(
                attrs={"class": "form-control", "required": False}
            ),
            "copyright_panels_text_1": forms.Textarea(
                attrs={
                    "class": "form-control h-auto fs-4",
                    "rows": 6,
                    "required": False,
                }
            ),
            "copyright_panels_text_2": forms.Textarea(
                attrs={
                    "class": "form-control h-auto fs-4",
                    "rows": 6,
                    "required": False,
                }
            ),
            "copyright_panels_link_text": forms.TextInput(
                attrs={"class": "form-control fs-5", "required": True}
            ),
            "copyright_panels_link_url": forms.URLInput(
                attrs={"class": "form-control", "required": False}
            ),
            "sort_order": forms.NumberInput(
                attrs={"class": "form-control", "required": False}
            ),
            "is_main": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "description": CKEditor5Widget(),
        }
