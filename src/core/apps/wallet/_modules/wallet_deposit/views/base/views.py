from ...models import models as mm


def get_wallet_deposit_model():
    return mm.WalletDeposit


def get_wallet_deposit_objects():
    return get_wallet_deposit_model().objects


def get_wallet_deposit_with_pk(pk):
    return get_wallet_deposit_objects().filter(pk__iexact=str(pk)).first()


def get_wallet_deposit_first():
    return get_wallet_deposit_objects().first()


def get_wallet_deposit_last():
    return get_wallet_deposit_objects().last()


def get_wallet_deposits_all():
    return get_wallet_deposit_objects().all()
