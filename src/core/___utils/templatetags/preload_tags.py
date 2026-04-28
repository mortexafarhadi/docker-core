from django import template
from django.templatetags.static import static

register = template.Library()


@register.simple_tag
def preload_font(font_path, font_type="woff2"):
    """
    ایجاد تگ preload برای فونت‌ها
    """
    return f'<link rel="preload" href="{static(font_path)}" as="font" type="font/{font_type}" crossorigin>'


@register.simple_tag
def preload_image(image_path, image_type=None):
    """
    ایجاد تگ preload برای تصاویر
    """
    type_attr = f' type="image/{image_type}"' if image_type else ""
    return f'<link rel="preload" href="{static(image_path)}" as="image"{type_attr}>'


@register.simple_tag
def preload_script(script_path):
    """
    ایجاد تگ preload برای اسکریپت‌ها
    """
    return f'<link rel="preload" href="{static(script_path)}" as="script">'


@register.simple_tag
def preload_style(style_path):
    """
    ایجاد تگ preload برای استایل‌ها
    """
    return f'<link rel="preload" href="{static(style_path)}" as="style" onload="this.rel=\'stylesheet\'">'


@register.simple_tag
def preload_video(video_path, video_type="mp4"):
    """
    ایجاد تگ preload برای ویدیوها
    """
    return f'<link rel="preload" href="{static(video_path)}" as="video" type="video/{video_type}">'


@register.simple_tag
def preload_audio(audio_path, audio_type="mp3"):
    """
    ایجاد تگ preload برای فایل‌های صوتی
    """
    return f'<link rel="preload" href="{static(audio_path)}" as="audio" type="audio/{audio_type}">'
