from ...models.models import RegisterUser


def get_register_user_model():
    return RegisterUser


def get_register_user_objects():
    return get_register_user_model().objects


def get_register_user_with_id(pk):
    return get_register_user_objects().filter(id__iexact=str(pk)).first()


def get_register_user_with_email(email):
    return get_register_user_objects().filter(email__iexact=str(email)).first()


def get_register_user_with_phone(phone):
    return get_register_user_objects().filter(phone__iexact=str(phone)).first()


def get_register_user_with_activation_code(activation_code):
    return (
        get_register_user_objects()
        .filter(activation_code__iexact=str(activation_code))
        .first()
    )


def get_register_user_none():
    return get_register_user_objects().none()


def get_register_user_first():
    return get_register_user_objects().first()


def get_register_user_last():
    return get_register_user_objects().last()


def get_register_users_all():
    return get_register_user_objects().all()
