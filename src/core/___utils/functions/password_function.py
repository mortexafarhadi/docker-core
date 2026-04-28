from decouple import config

SALT_PASSWORD = config("SALT_PASSWORD", default="")


def get_salt_password():
    return SALT_PASSWORD


def set_salt_password(password):
    return f"{get_salt_password()}{password}{get_salt_password()}"
