from _0_utils.functions.queryset_function import random_choice_queryset
from ...models import models as mm


def get_category_model():
    return mm.Category


def get_category_objects():
    return get_category_model().objects


def get_category_first():
    return get_category_objects().first()


def get_category_last():
    return get_category_objects().last()


def get_categories_all():
    return get_category_objects().all()


def get_category_with_pk(pk):
    return get_category_objects().filter(id__iexact=str(pk)).first()


def get_categories_active(status=True, queryset=get_category_objects()):
    return queryset.filter(is_active=status)


def get_category_active__random(status=True, queryset=None):
    if queryset is None:
        queryset = get_categories_active(status=status)
    return random_choice_queryset(queryset=queryset)


def get_categories_deleted(status=True, queryset=get_category_objects()):
    return queryset.filter(is_deleted=status)
