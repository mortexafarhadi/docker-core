from ...models import models as mm


def get_social_network_model():
    return mm.SocialNetwork


def get_social_network_objects():
    return get_social_network_model().objects


def get_social_network_first():
    return get_social_network_objects().first()


def get_social_network_last():
    return get_social_network_objects().last()


def get_social_networks_all():
    return get_social_network_objects().all()


def get_social_network_with_pk(pk):
    return get_social_network_objects().filter(id__iexact=str(pk)).first()


def get_social_networks_active(status=True, queryset=get_social_network_objects()):
    return queryset.filter(is_active=status)


def get_social_networks_deleted(status=True, queryset=get_social_network_objects()):
    return queryset.filter(is_deleted=status)
