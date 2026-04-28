from django import template

register = template.Library()


@register.inclusion_tag("path_to.html")
def base_inclusion_tag():
    """
    for use most load file name
        # like {% load inclusion_tags %}
    and call function name in html
        # like {% base_inclusion_tag %}
    """
    test = 0
    return {"test": test}


@register.inclusion_tag("path_to.html")
def base_inclusion_tag_with_data(object_id):
    """
    for use most load file name
        # like {% load inclusion_tags %}
    and call function name in html
        # like {% base_inclusion_tag object.id %}
    """
    # categories = Product.objects.filter(category_id = object_id)
    # return {'categories': categories}
    pass
