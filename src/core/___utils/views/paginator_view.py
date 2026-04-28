from django.core.paginator import Paginator


def get_page_range(current_page, total_page, count=7):
    if count % 2 == 0:
        count = 7
    half_count = count // 2
    if total_page <= count:
        return list(range(1, total_page + 1))
    if current_page <= half_count + 1:
        return list(range(1, count + 1))
    if current_page >= total_page - half_count:
        return list(range(total_page - count + 1, total_page + 1))
    return list(range(current_page - half_count, current_page + half_count + 1))


def paginate_queryset(
    context, queryset, page=1, page_size=10, order_by="id", reverse=False
):
    try:
        page = int(page) if page else 1
    except (ValueError, TypeError):
        page = 1

    try:
        page_size = int(page_size) if page_size else 10
    except (ValueError, TypeError):
        page_size = 10

    if hasattr(queryset, "order_by"):
        ordering = f"-{order_by}" if reverse else order_by
        queryset = queryset.order_by(ordering)
    else:
        queryset = sorted(
            queryset, key=lambda item: item.get(order_by, 0), reverse=reverse
        )

    paginator = Paginator(queryset, page_size)
    page_obj = paginator.get_page(page)

    context.update(
        {
            "paginator": paginator,
            "page_obj": page_obj,
            "is_paginated": page_obj.has_other_pages(),
            "object_list": page_obj.object_list,
            "page_range": get_page_range(
                current_page=page_obj.number, total_page=paginator.num_pages
            ),
        }
    )

    return context
