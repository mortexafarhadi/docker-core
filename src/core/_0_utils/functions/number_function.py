import random
from decimal import Decimal, InvalidOperation, ROUND_CEILING
from typing import Any, Optional

from faker import Faker


def random_number_fix_len(digits=10):
    return Faker().random_number(digits=digits, fix_len=True)


def round_up(number, multiple=1):
    n = Decimal(str(number))
    m = Decimal(str(multiple))

    if m <= 0:
        raise ValueError("multiple must be positive")

    q = (n / m).to_integral_value(rounding=ROUND_CEILING)
    result = q * m

    exp = -m.as_tuple().exponent if m != m.to_integral() else 0

    return result.quantize(Decimal(1).scaleb(-exp))


def decimal_places(n: int) -> Decimal:
    if n < 0:
        raise ValueError("n must be non-negative")

    return Decimal("1").scaleb(-n)


def random_int_range(min_val, max_val):
    return random.randint(int(min_val), int(max_val))


def random_float_range(min_val, max_val):
    return random.uniform(float(min_val), float(max_val))


def calc_percent(value, percent, convert_to_decimal=False):
    try:
        _result = (float(value) * float(percent)) / 100
        return to_decimal(_result) if convert_to_decimal else _result
    except ValueError:
        raise ValueError("value and percent must be numbers")


def to_decimal(
    value: Any,
    *,
    default: Optional[Decimal] = None,
    strip_commas: bool = True,
    allow_none: bool = False,
) -> Decimal:
    """
    تبدیل امن انواع متداول به Decimal.

    پارامترها:
      - value: هر نوع ورودی (Decimal/int/float/str/bool/None/...)
      - default: مقدار بازگشتی در صورت نامعتبر بودن ورودی (اگر None باشد، Exception raise می‌شود)
      - strip_commas: اگر True باشد، در رشته‌ها ',' حذف می‌شود (برای "1,234.56")
      - allow_none: اگر True و value=None باشد، None برمی‌گرداند؛ در غیر این صورت خطا یا default

    رفتار:
      - Decimal -> همان مقدار
      - None -> اگر allow_none=True: None، وگرنه default یا خطا
      - bool -> به int تبدیل می‌شود (True -> 1, False -> 0)
      - int -> مستقیم به Decimal
      - float -> ابتدا با نمای دقیق به str تبدیل می‌شود تا خطای شناوری وارد Decimal نشود
      - str -> trim و در صورت نیاز حذف کاما؛ سپس تبدیل به Decimal
      - سایر انواع -> ابتدا به str تبدیل می‌شوند و سپس تلاش برای Decimal

    Raises:
      - ValueError: اگر تبدیل ممکن نباشد و default تعیین نشده باشد
    """
    # 1) اگر خود Decimal است
    if isinstance(value, Decimal):
        return value

    # 2) None
    if value is None:
        if allow_none:
            return None  # type: ignore[return-value]
        if default is not None:
            return default
        raise ValueError("to_decimal: value is None and no default provided")

    # 3) Bool (زیرکلاس int است، ولی رفتار صریح‌تر بهتر است)
    if isinstance(value, bool):
        return Decimal(int(value))

    # 4) اعداد صحیح
    if isinstance(value, int):
        return Decimal(value)

    # 5) اعداد اعشاری float
    if isinstance(value, float):
        # تبدیل دقیق به رشته برای پرهیز از خطای باینری float
        # از repr/format استفاده می‌کنیم
        s = format(value, ".15g")  # دقت مناسب برای بیشتر کاربردها
        try:
            return Decimal(s)
        except InvalidOperation:
            if default is not None:
                return default
            raise ValueError(f"to_decimal: cannot convert float {value!r} to Decimal")

    # 6) رشته‌ها و سایر انواع (با تبدیل به str)
    s = str(value).strip()

    # اگر رشته خالی است
    if s == "":
        if default is not None:
            return default
        raise ValueError("to_decimal: empty string cannot be converted to Decimal")

    # حذف جداکننده هزارگان
    if strip_commas:
        s = s.replace(",", "")

    try:
        return Decimal(s)
    except InvalidOperation:
        if default is not None:
            return default
        raise ValueError(f"to_decimal: cannot convert {value!r} to Decimal")
