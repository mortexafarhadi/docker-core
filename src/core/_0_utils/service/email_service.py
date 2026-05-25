from _0_utils.functions.string_function import print_debug, red_text, blue_text, green_text
from _1_site_setting.views.base.views_base import site_setting_context
from decouple import config
from django.conf import settings
from django.core.mail import send_mail as email_service
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from celery import shared_task

USE_EMAIL_SERVICE = config("USE_EMAIL_SERVICE", default=False, cast=bool)


def send_mail(subject, email, context, template):
    if not USE_EMAIL_SERVICE:
        msg = green_text(f"USE_EMAIL_SERVICE Key in .env Config Not Set. code is : {context.get('code', 'not set')}")
        print(msg)
        return True, msg, "Email Service is not available"

    context = site_setting_context(context)
    _send_mail.delay(subject=subject, to=email, context=context, template_name=template)
    print_debug("Mail Sent Successfully")
    return True, "Mail Sent Successfully", None


@shared_task()
def _send_mail(subject, to, context, template_name):
    try:
        html_message = render_to_string(template_name, context)
        plain_message = strip_tags(html_message)
        from_email = settings.DEFAULT_FROM_EMAIL

        email_service(
            subject=subject,
            message=plain_message,
            from_email=from_email,
            recipient_list=[to],
            html_message=html_message,
        )
        print(f"Sent Mail Successfully to: {to}")
    except Exception as e:
        print(blue_text("*" * 50))
        print(red_text(e))
        print(blue_text("*" * 50))


def send_mail_without_queue(subject, email, context, template):
    if not USE_EMAIL_SERVICE:
        msg = f"USE_EMAIL_SERVICE Key in .env Config Not Set. code is : {context.get('code', 'not set')}"
        print(msg)
        return True, msg, "Email Service is not available"
    else:
        context = site_setting_context(context)
        status, msg, error = _send_mail_without_queue(
            subject=subject, to=email, context=context, template_name=template
        )
        return status, msg, error


def _send_mail_without_queue(subject, to, context, template_name):
    try:
        html_message = render_to_string(template_name, context)
        plain_message = strip_tags(html_message)
        from_email = settings.DEFAULT_FROM_EMAIL
        email_service(
            subject=subject,
            message=plain_message,
            from_email=from_email,
            recipient_list=[to],
            html_message=html_message,
        )
        return True, "Mail Sent Successfully", None
    except Exception as e:
        print("*" * 50)
        print_debug(e)
        print("*" * 50)
        return False, "Mail Don't Send", e
