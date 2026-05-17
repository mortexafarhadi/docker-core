from sorl.thumbnail import get_thumbnail

from _0_utils.functions.generator.url_image_base import media_url


def get_image_thumbnail_setting(pic):
    if pic is None or pic == "" or not pic:
        return None
    else:
        thumbnail = get_thumbnail(pic, "512x512", quality=70, format="PNG")
        return media_url(thumbnail.url)
