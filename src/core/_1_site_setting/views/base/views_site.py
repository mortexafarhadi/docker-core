from ...models import models as mm


def get_site_setting_model():
    return mm.SiteSetting


def get_site_setting_objects():
    return get_site_setting_model().objects


def get_site_setting_none():
    return get_site_setting_objects().none()


def get_site_setting_first():
    return get_site_setting_objects().first()


def get_site_setting_last():
    return get_site_setting_objects().last()


def get_site_settings_all():
    return get_site_setting_objects().all()


def get_site_setting_site_choices():
    return get_site_setting_model().SITE_TYPES_CHOICES.choices


def get_site_setting_site_type_main():
    return get_site_setting_model().SITE_TYPES_CHOICES.MAIN


def get_site_setting_site_type_admin():
    return get_site_setting_model().SITE_TYPES_CHOICES.ADMIN


def get_site_setting_site_type_landing():
    return get_site_setting_model().SITE_TYPES_CHOICES.LANDING


def get_site_setting_with_pk(pk):
    return get_site_setting_objects().filter(id__iexact=str(pk)).first()


def get_site_settings_main(status=True, queryset=get_site_setting_objects()):
    return queryset.filter(site_type=get_site_setting_site_type_main(), is_main=status)


def get_site_settings_admin(status=True, queryset=get_site_setting_objects()):
    return queryset.filter(site_type=get_site_setting_site_type_admin(), is_main=status)


def get_site_settings_landing(status=True, queryset=get_site_setting_objects()):
    return queryset.filter(
        site_type=get_site_setting_site_type_landing(), is_main=status
    )


def get_site_setting_main(status=True, queryset=get_site_setting_objects()):
    return get_site_settings_main(status, queryset).order_by("-datetime_update").first()


def get_site_setting_admin(status=True, queryset=get_site_setting_objects()):
    return (
        get_site_settings_admin(status, queryset).order_by("-datetime_update").first()
    )


def get_site_setting_landing(status=True, queryset=get_site_setting_objects()):
    return (
        get_site_settings_landing(status, queryset).order_by("-datetime_update").first()
    )


def get_site_settings_deleted(status=True, queryset=get_site_setting_objects()):
    return queryset.filter(is_deleted=status)
