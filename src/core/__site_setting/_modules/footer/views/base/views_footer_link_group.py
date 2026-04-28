from ...models import models as mm


def get_footer_link_group_model():
    return mm.FooterLinkGroup


def get_footer_link_group_objects():
    return get_footer_link_group_model().objects


def get_footer_link_group_none():
    return get_footer_link_group_objects().none()


def get_footer_link_group_first():
    return get_footer_link_group_objects().first()


def get_footer_link_group_last():
    return get_footer_link_group_objects().last()


def get_footer_link_groups_all():
    return get_footer_link_group_objects().all()


def get_footer_link_group_with_pk(pk):
    return get_footer_link_group_objects().filter(id__iexact=str(pk)).first()


def get_footer_link_groups_active(
    status=True, queryset=get_footer_link_group_objects()
):
    return queryset.filter(is_active=status)


def get_footer_link_groups_deleted(
    status=True, queryset=get_footer_link_group_objects()
):
    return queryset.filter(is_deleted=status)


def get_footer_link_group_with_title(title):
    return get_footer_link_group_objects().filter(title__iexact=str(title)).first()


def get_footer_link_group_with_link(link):
    return get_footer_link_group_objects().filter(link__iexact=str(link)).first()


def get_footer_link_groups_with_open_in_newtab(
    open_in_newtab=True, queryset=get_footer_link_group_objects()
):
    return queryset.filter(open_in_newtab=open_in_newtab)


def get_footer_link_groups_with_move_mode(
    move_mode=True, queryset=get_footer_link_group_objects()
):
    return queryset.filter(is_move_mode=move_mode)


def get_footer_link_groups_with_has_child(
    has_child=True, queryset=get_footer_link_group_objects()
):
    return queryset.filter(has_child=has_child)


def get_footer_link_groups_active_prefetch_footer_link(status=True):
    return get_footer_link_groups_active(status).prefetch_related("parent")


def get_footer_link_groups_active_with_has_child(status=True, has_child=True):
    return get_footer_link_groups_with_has_child(
        has_child, get_footer_link_groups_active(status)
    )
