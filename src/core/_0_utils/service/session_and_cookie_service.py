from datetime import datetime
from typing import Optional


def get_session_key(request, key, default=None):
    return request.session.get(key, default)


def set_session_key(request, key, value):
    request.session[key] = str(value)


def get_cookie_key(request, key, default=None):
    return request.COOKIES.get(key, default)


def set_cookie_key(
    response,
    key: str,
    value,
    max_age: Optional[int] = None,
    expires: Optional[datetime or str] = None,
    path: str = "/",
    domain: Optional[str] = None,
    secure: bool = False,
    httponly: bool = False,
    samesite: str = "Lax",
) -> None:
    """
    تابعی جامع برای تنظیم کوکی در پاسخ HTTP جنگو.

    :param response: شیء HttpResponse که کوکی باید به آن اضافه شود.
    :param key: (ضروری) نام کوکی.
    :param value: (ضروری) مقدار کوکی (به طور خودکار به str تبدیل می‌شود).
    :param max_age: (اختیاری) حداکثر عمر کوکی بر حسب ثانیه. اگر None باشد، کوکی تا بسته شدن مرورگر معتبر است.
    :param expires: (اختیاری) تاریخ و زمان دقیق انقضای کوکی (شیء datetime یا رشته در فرمت GMT).
                    اگر هر دو max_age و expires تنظیم شوند، expires اولویت دارد.
    :param path: (اختیاری) مسیری در دامنه که کوکی برای آن معتبر است. پیش‌فرض: '/'.
    :param domain: (اختیاری) دامنه‌ای که کوکی برای آن معتبر است (مثلاً '.example.com').
                   اگر None باشد، کوکی فقط برای دامنه فعلی معتبر است.
    :param secure: (اختیاری) اگر True باشد، کوکی فقط از طریق HTTPS ارسال می‌شود. پیش‌فرض: False.
    :param httponly: (اختیاری) اگر True باشد، کوکی فقط توسط سرور قابل دسترسی است و JavaScript نمی‌تواند به آن دسترسی داشته باشد. پیش‌فرض: False.
    :param samesite: (اختیاری) کنترل نحوه ارسال کوکی در درخواست‌های Cross-Site. مقادیر ممکن: 'Lax', 'Strict', 'None'.
                     توجه: اگر 'None' باشد، secure باید True باشد.
                     پیش‌فرض: 'Lax'.
    """

    cookie_args = {
        "key": key,
        "value": str(value),
        "path": path,
        "secure": secure,
        "httponly": httponly,
        "samesite": samesite,
    }

    if max_age is not None:
        cookie_args["max_age"] = max_age

    if expires is not None:
        cookie_args["expires"] = expires

    if domain is not None:
        cookie_args["domain"] = domain

    if samesite == "None" and not cookie_args["secure"]:
        print(
            "هشدار: برای samesite='None'، کوکی باید secure=True باشد. این مقدار به True تغییر داده شد."
        )
        cookie_args["secure"] = True

    response.set_cookie(**cookie_args)
