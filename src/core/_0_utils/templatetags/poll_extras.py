from datetime import datetime
from urllib.parse import urlparse, parse_qs, urlencode

from django import template
from django.template.defaultfilters import stringfilter
from jalali_date import date2jalali

from _0_utils.functions.number_function import round_up, decimal_places

register = template.Library()


@register.filter(is_safe=False)
@stringfilter
def make_list_by_comma(value):
    return value.split(",")


@register.filter
def check_in_list_str(value, list_str, *args, **kwargs):
    _list = make_list_by_comma(list_str)
    for item in _list:
        if item in value:
            return True
    return False


@register.filter(is_safe=False)
@stringfilter
def make_range(value):
    return list(range(int(value)))


# @register.filter(name='to_jalali')
# def to_jalali(value):
#     return date2jalali(value)


@register.filter(name="to_jalali")
def to_jalali(value):
    if not value:
        return ""
    if isinstance(value, str):
        try:
            value = datetime.strptime(value, "%Y-%m-%d %H:%M")
        except ValueError:
            return value
    try:
        return date2jalali(value).strftime("%Y/%m/%d")
    except Exception as e:
        print(e)
        return value


@register.filter(name="fix_url")
def fix_url(url):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    filtered_params = {
        k: v for k, v in query_params.items() if v and v[0] and k != "page"
    }
    new_query_string = urlencode(filtered_params, doseq=True)
    result = f"?{new_query_string}" if new_query_string else ""
    return result


@register.filter(name="separate_number")
def separate_number(number, floating_number=-1):
    if number is None or number == "":
        return "0"
    else:
        if floating_number != -1:
            number = round_up(number, decimal_places(floating_number))
        whole_number, decimal_part = split_number(number)
        res = "{:,}".format(whole_number) if whole_number > 0 else "0"
        return f"{res}.{decimal_part}" if decimal_part != "0" else res


@register.filter(name="separate_with_dash")
def separate_with_dash(number, digits=4, space_number=1):
    space = " " * space_number
    number_str = str(number)
    number_str = number_str.replace(" ", "")
    parts = []

    for i in range(0, len(number_str), digits):
        part = number_str[i : i + digits]
        parts.append(part)

    if len(number_str) % digits != 0:
        remaining_part = number_str[len(number_str) - (len(number_str) % digits) :]
        parts.append(remaining_part)

    z = f"{space}-{space}"
    return z.join(parts)


@register.filter(name="cut")
def cut(value, arg):
    return value.replace(arg, "")


@register.filter(name="get_type")
def get_type(value):
    return type(value)


@register.filter(name="three_digit_currency_toman")
def three_digit_currency_dollar(value: int):
    return "$ " + "{:,}".format(value)


@register.filter(name="three_digit_currency_toman")
def three_digit_currency_toman(value: int):
    return "{:,}".format(value) + " تومان"


@register.simple_tag
def multiply(quantity, price, *args, **kwargs):
    return three_digit_currency_toman(quantity * price)


def split_number(number):
    x = str(number)
    has_decimal_part = x.find(".")
    if has_decimal_part != -1:
        decimal_part = x[x.find(".") + 1 :]
    else:
        decimal_part = "0"
    whole_number = int(number)
    while decimal_part != "0" and decimal_part[-1] == "0":
        decimal_part = decimal_part[:-1]
    return whole_number, decimal_part


def float_number(number):
    res = float(number)
    return int(res) if res.is_integer() else res


@register.filter
def subtract(value, arg):
    try:
        return value - arg
    except (ValueError, TypeError):
        return ""  # Or handle the error as needed
