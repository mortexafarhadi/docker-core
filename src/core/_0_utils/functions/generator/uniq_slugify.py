import re

from slugify import slugify

# فرض بر این است که این متدها در مسیرهای گفته شده وجود دارند
from _0_utils.functions.number_function import random_number_fix_len
from _0_utils.functions.string_function import (
    replace_space_to_dash,
    replace_dot_to_dash,
    random_string,
    get_substring_zero_to_find,
    replace_space_dot_at_to_dash,
)


def is_value_taken(instance, field_name, value):
    """بررسی وجود مقدار در دیتابیس با در نظر گرفتن خودِ آبجکت (برای آپدیت)"""
    Klass = instance.__class__
    qs = Klass.objects.filter(**{f"{field_name}__iexact": str(value)})
    if instance.pk:
        qs = qs.exclude(pk=instance.pk)
    return qs.exists()


def generate_unique_slug(
    instance,
    text,
    field,
    safe_chars=["-"],
    pre_process_func=None,
    postfix_func=None,
):
    if pre_process_func:
        text = pre_process_func(text)

    # استفاده از Raw String برای جلوگیری از SyntaxWarning در پایتون 3.12
    safe_pattern = "".join([re.escape(c) for c in safe_chars])
    custom_regex = r"[^-a-z0-9" + safe_pattern + r"]+"

    # تولید اسلاگ پایه
    base_slug = slugify(text, regex_pattern=custom_regex, lowercase=True)

    # اگر متن ورودی خالی بود یا کاراکتر معتبری نداشت
    if not base_slug:
        base_slug = "unknown"

    result = base_slug
    while is_value_taken(instance, field, result):
        postfix = postfix_func() if postfix_func else random_string(4)
        result = f"{base_slug}-{postfix}"

    return result


def uniq_slugify_slug_safe_dash_dot_at(instance, text):
    return generate_unique_slug(
        instance,
        text,
        field="slug",
        safe_chars=["-", ".", "@"],
        pre_process_func=replace_space_dot_at_to_dash,
    )


def uniq_slugify_slug_safe_dot_at(instance, text):
    return generate_unique_slug(
        instance,
        text,
        field="slug",
        safe_chars=[".", "@"],
        pre_process_func=replace_space_dot_at_to_dash,
    )


def uniq_slugify_slug_safe_dash(instance, text):
    return generate_unique_slug(
        instance,
        text,
        field="slug",
        safe_chars=["-"],
        pre_process_func=replace_space_dot_at_to_dash,
    )


def uniq_slugify_code_safe_dash(instance, text):
    return generate_unique_slug(
        instance,
        text,
        field="code",
        safe_chars=["-"],
        pre_process_func=replace_space_dot_at_to_dash,
    )


def uniq_slugify_username_rplc_space_dot(instance, text):
    def preprocess(txt):
        txt = get_substring_zero_to_find(txt, "@")
        txt = replace_space_to_dash(txt)
        txt = replace_dot_to_dash(txt)
        return txt

    return generate_unique_slug(
        instance,
        text,
        field="username",
        safe_chars=["-"],
        pre_process_func=preprocess,
    )


# --- Number & Code Generators ---


def generate_unique_number(
    instance, field, value=None, prefix="", digits=10, _random=3
):
    # اگر مقداری پاس داده شده، ابتدا همان را چک کن، در غیر این صورت عدد تصادفی بساز
    current_value = (
        f"{prefix}{value if value is not None else random_number_fix_len(digits)}"
    )

    while is_value_taken(instance, field, current_value):
        if value is not None:
            # اگر مقدار اولیه تکراری بود، به انتهای آن عدد تصادفی اضافه کن
            current_value = f"{value}{random_number_fix_len(_random)}"
        else:
            # اگر کلاً تصادفی بود، دوباره عدد تصادفی جدید بساز
            current_value = f"{prefix}{random_number_fix_len(digits)}"

    return current_value


def generate_unique_string(
    instance, field, value=None, prefix="", length=10, _random=3
):
    # اگر مقداری پاس داده شده، ابتدا همان را چک کن، در غیر این صورت عدد تصادفی بساز
    current_value = f"{prefix}{value if value is not None else random_string(length)}"

    while is_value_taken(instance, field, current_value):
        if value is not None:
            # اگر مقدار اولیه تکراری بود، به انتهای آن عدد تصادفی اضافه کن
            current_value = f"{value}{random_string(_random)}"
        else:
            # اگر کلاً تصادفی بود، دوباره عدد تصادفی جدید بساز
            current_value = f"{prefix}{random_string(length)}"

    return current_value


def uniq_number_username(instance, digits=10):
    return generate_unique_number(instance, "username", digits=digits)


def uniq_number_code(instance, prefix="", digits=10):
    return generate_unique_number(instance, "code", prefix=prefix, digits=digits)


def uniq_str_code(instance, prefix="", length=10):
    return generate_unique_string(instance, "code", prefix=prefix, length=length)


def uniq_number_slug(instance, prefix="", digits=20):
    return generate_unique_number(instance, "slug", prefix=prefix, digits=digits)


def uniq_number_token(instance, prefix="", digits=20):
    return generate_unique_number(instance, "token", prefix=prefix, digits=digits)


def uniq_number_activation_code(instance, digits=20):
    return generate_unique_number(instance, "activation_code", digits=digits)


def uniq_str_referral_code(instance, digits=6):
    while True:
        code = random_string(digits).upper()
        if not is_value_taken(instance, "referral_code", code):
            return code
