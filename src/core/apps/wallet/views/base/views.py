from ___utils.functions.list_and_dict_function import check_and_get_list
from ...models import models as mm


def get_wallet_model():
    return mm.Wallet


def get_wallet_objects():
    return get_wallet_model().objects


def get_wallet_none():
    return get_wallet_objects().none()


def get_wallet_first():
    return get_wallet_objects().first()


def get_wallet_last():
    return get_wallet_objects().last()


def get_wallets_all():
    return get_wallet_objects().all()


def get_wallet_with_pk(pk):
    return get_wallet_objects().filter(pk__iexact=str(pk)).first()


def get_wallets_active(status=True, queryset=get_wallet_objects()):
    return queryset.filter(is_active=status)


def get_wallets_deleted(status=True, queryset=get_wallet_objects()):
    return queryset.filter(is_deleted=status)


def get_wallets_with_user_object__in(user_list, queryset=get_wallet_objects()):
    return queryset.filter(user__in=check_and_get_list(user_list))


def get_wallets_with_user_username__in(
    user_username_list, queryset=get_wallet_objects()
):
    return queryset.filter(user__username__in=check_and_get_list(user_username_list))


def create_wallet_with_user_object(user):
    return get_wallet_objects().create(user=user)
