from ...models.models import UserSetting


def get_user_setting_model():
    return UserSetting


def get_user_setting_objects():
    return get_user_setting_model().objects


def get_user_setting_with_user_object(user):
    return get_user_setting_objects().filter(user=user).first()


def get_user_setting_with_user_username(user_username):
    return get_user_setting_objects().filter(user__username=user_username).first()


def get_user_setting_none():
    return get_user_setting_objects().none()


def get_user_setting_first():
    return get_user_setting_objects().first()


def get_user_setting_last():
    return get_user_setting_objects().last()


def get_user_setting_all():
    return get_user_setting_objects().all()
