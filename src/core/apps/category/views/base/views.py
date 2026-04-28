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


def get_categories_deleted(status=True, queryset=get_category_objects()):
    return queryset.filter(is_deleted=status)
