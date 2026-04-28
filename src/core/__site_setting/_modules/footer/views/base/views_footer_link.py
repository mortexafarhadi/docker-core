from ...models import models as mm


def get_footer_link_model():
    return mm.FooterLink


def get_footer_link_objects():
    return get_footer_link_model().objects


def get_footer_link_none():
    return get_footer_link_objects().none()


def get_footer_link_first():
    return get_footer_link_objects().first()


def get_footer_link_last():
    return get_footer_link_objects().last()


def get_footer_links_all():
    return get_footer_link_objects().all()


def get_footer_link_with_pk(pk):
    return get_footer_link_objects().filter(id__iexact=str(pk)).first()


def get_footer_links_active(status=True, queryset=get_footer_link_objects()):
    return queryset.filter(is_active=status)


def get_footer_links_deleted(status=True, queryset=get_footer_link_objects()):
    return queryset.filter(is_deleted=status)


def get_footer_link_with_title(title):
    return get_footer_link_objects().filter(title__iexact=str(title)).first()


def get_footer_link_with_link(link):
    return get_footer_link_objects().filter(link__iexact=str(link)).first()


def get_footer_links_with_open_in_newtab(
    open_in_newtab=True, queryset=get_footer_link_objects()
):
    return queryset.filter(open_in_newtab=open_in_newtab)
