from ...models.models import HeaderLink


def get_header_link_model():
    return HeaderLink.objects


def get_header_link_none():
    return get_header_link_model().none()


def get_header_link_with_pk(pk):
    return get_header_link_model().filter(id__iexact=str(pk)).first()


def get_header_link_first():
    return get_header_link_model().first()


def get_header_link_last():
    return get_header_link_model().last()


def get_header_links_all():
    return get_header_link_model().all()


def get_header_links_active(status=True, queryset=get_header_link_model()):
    return queryset.filter(is_active=status)


def get_header_links_deleted(status=True, queryset=get_header_link_model()):
    return queryset.filter(is_deleted=status)


def get_header_link_with_title(title):
    return get_header_link_model().filter(title__iexact=str(title)).first()


def get_header_link_with_link(link):
    return get_header_link_model().filter(link__iexact=str(link)).first()


def get_header_links_with_open_in_newtab(
    open_in_newtab=True, queryset=get_header_link_model()
):
    return queryset.filter(open_in_newtab=open_in_newtab)
