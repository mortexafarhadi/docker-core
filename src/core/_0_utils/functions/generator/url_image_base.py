from sorl.thumbnail import get_thumbnail

from _0_utils.functions.generator.url_base import media_url


def get_image_thumbnail(pic):
    if pic is None or pic == "" or not pic:
        return None
    else:
        from _1_site_setting.views.base.views_site import get_site_setting_main

        setting = get_site_setting_main()
        quality = setting.thumbnail_quality if setting is not None else 70
        size = setting.thumbnail_size if setting is not None else "512x512"
        thumbnail = get_thumbnail(pic, size, quality=quality, format="PNG")
        return media_url(thumbnail.url)
