from ...models import models as mm


def get_wallet_withdrawal_model():
    return mm.WalletWithdrawal


def get_wallet_withdrawal_objects():
    return get_wallet_withdrawal_model().objects


def get_wallet_withdrawal_none():
    return get_wallet_withdrawal_objects().none()


def get_wallet_withdrawal_status_choice():
    return get_wallet_withdrawal_model().StatusChoices


def get_wallet_withdrawal_with_pk(pk):
    return get_wallet_withdrawal_objects().filter(pk__iexact=str(pk)).first()


def get_wallet_withdrawal_first():
    return get_wallet_withdrawal_objects().first()


def get_wallet_withdrawal_last():
    return get_wallet_withdrawal_objects().last()


def get_wallet_withdrawals_all():
    return get_wallet_withdrawal_objects().all()


def get_wallet_withdrawals_active(status=True, queryset=None):
    queryset = queryset if queryset is not None else get_wallet_withdrawal_objects()
    return queryset.filter(is_active=status)


def get_wallet_withdrawals_deleted(status=True, queryset=None):
    queryset = queryset if queryset is not None else get_wallet_withdrawal_objects()
    return queryset.filter(is_deleted=status)
