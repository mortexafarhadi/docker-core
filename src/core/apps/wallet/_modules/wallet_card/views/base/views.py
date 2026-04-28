from ...models import models as mm


def get_wallet_card_model():
    return mm.WalletCard


def get_wallet_card_objects():
    return get_wallet_card_model().objects


def get_wallet_card_none():
    return get_wallet_card_objects().none()


def get_wallet_card_with_pk(pk):
    return get_wallet_card_objects().filter(slug__iexact=str(pk)).first()


def get_wallet_card_first():
    return get_wallet_card_objects().first()


def get_wallet_card_last():
    return get_wallet_card_objects().last()


def get_wallet_cards_all():
    return get_wallet_card_objects().all()


def get_wallet_cards_active(status=True, queryset=None):
    queryset = queryset if queryset is not None else get_wallet_card_objects()
    return queryset.filter(is_active=status)


def get_wallet_cards_deleted(status=True, queryset=None):
    queryset = queryset if queryset is not None else get_wallet_card_objects()
    return queryset.filter(is_deleted=status)


def get_wallet_cards_main(status=True, queryset=None):
    queryset = queryset if queryset is not None else get_wallet_card_objects()
    return queryset.filter(is_main=status)


def get_wallet_cards_with_wallet(wallet, queryset=None):
    queryset = queryset if queryset is not None else get_wallet_card_objects()
    return queryset.filter(wallet=wallet)
