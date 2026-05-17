from _0_utils.functions.list_and_dict_function import check_and_get_list
from ...models import models as mm


def get_user_model():
    return mm.User


def get_user_objects():
    return get_user_model().objects


def get_user_none():
    return get_user_objects().none()


def get_user_first():
    return get_user_objects().first()


def get_user_last():
    return get_user_objects().last()


def get_users_all():
    return get_user_objects().all()


def get_user_gender_choices():
    return mm.User.GENDER_CHOICES.choices


def get_user_gender_not_selected():
    return mm.User.GENDER_CHOICES.NOT_SELECTED


def get_user_gender_male():
    return mm.User.GENDER_CHOICES.MALE


def get_user_gender_female():
    return mm.User.GENDER_CHOICES.FEMALE


def get_user_with_code(code):
    return get_user_objects().filter(code__iexact=str(code)).first()


def get_user_with_code__in(code_list):
    return get_user_objects().filter(code__in=check_and_get_list(code_list))


def get_user_with_email(email):
    return get_user_objects().filter(email__iexact=str(email)).first()


def get_user_with_email__in(email_list):
    return get_user_objects().filter(email__in=check_and_get_list(email_list))


def get_user_with_phone(phone):
    return get_user_objects().filter(phone__iexact=str(phone)).first()


def get_user_with_phone__in(phone_list):
    return get_user_objects().filter(phone__in=check_and_get_list(phone_list))


def get_user_with_username(username):
    return get_user_objects().filter(username__iexact=str(username)).first()


def get_user_with_username__in(username_list):
    return get_user_objects().filter(username__in=check_and_get_list(username_list))


def get_user_with_reset_password_link(reset_password_link):
    return (
        get_user_objects()
        .filter(reset_password_link__iexact=str(reset_password_link))
        .first()
    )


def get_users_active(status=True, queryset=get_user_objects()):
    return queryset.filter(is_active=status)


def get_users_deleted(status=True, queryset=get_user_objects()):
    return queryset.filter(is_deleted=status)
