from _0_utils.functions.list_and_dict_function import check_and_get_list
from ...models.models import UserSocialMedia


def get_user_social_media_model():
    return UserSocialMedia


def get_user_social_media_objects():
    return get_user_social_media_model().objects


def get_user_social_media_none():
    return get_user_social_media_objects().none()


def get_user_social_media_with_id(pk):
    return get_user_social_media_objects().filter(id__iexact=str(pk)).first()


def get_user_social_media_first():
    return get_user_social_media_objects().first()


def get_user_social_media_last():
    return get_user_social_media_objects().last()


def get_user_social_medias_all():
    return get_user_social_media_objects().all()


def get_user_social_medias_active(status=True, queryset=None):
    queryset = queryset if queryset is not None else get_user_social_media_objects()
    return queryset.filter(is_active=status)


def get_user_social_medias_deleted(status=True, queryset=None):
    queryset = queryset if queryset is not None else get_user_social_media_objects()
    return queryset.filter(is_deleted=status)


def get_user_social_medias_with_user_object_in(user_list, queryset=None):
    user_list = check_and_get_list(user_list)
    queryset = queryset if queryset is not None else get_user_social_media_objects()
    return queryset.filter(user__in=user_list)


def get_user_social_medias_with_user_username_in(user_username_list, queryset=None):
    user_username_list = check_and_get_list(user_username_list)
    queryset = queryset if queryset is not None else get_user_social_media_objects()
    return queryset.filter(user__username__in=user_username_list)


def get_user_social_medias_with_social_network_object_in(
    social_network_list, queryset=None
):
    social_network_list = check_and_get_list(social_network_list)
    queryset = queryset if queryset is not None else get_user_social_media_objects()
    return queryset.filter(social_network__in=social_network_list)


def get_user_social_medias_with_social_network_id_in(
    social_network_id_list, queryset=None
):
    social_network_id_list = check_and_get_list(social_network_id_list)
    queryset = queryset if queryset is not None else get_user_social_media_objects()
    return queryset.filter(social_network__id__in=social_network_id_list)


def get_user_social_medias_with_user_object_social_network_object_in(
    user_list, social_network_list, queryset=None
):
    queryset = get_user_social_medias_with_user_object_in(user_list, queryset)
    return get_user_social_medias_with_social_network_object_in(
        social_network_list, queryset
    )
