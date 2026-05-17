import re

from django.utils.crypto import get_random_string

from _0_utils.base_variables import SHOW_LOG_DEBUG


class TextColors:
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    RESET = "\033[0m"


def print_debug(value, _function=None):
    if SHOW_LOG_DEBUG:
        if _function:
            print(f"{_function}: {value}")
        else:
            print(f"{value}")


def text_to_bytes(text: str):
    return text.encode("utf-8")


def bytes_to_text(byte_string: bytes):
    return byte_string.decode("utf-8")


def zfill(value, length=3, symbol="0"):
    value = str(value)
    while len(value) < length:
        value = symbol + value
    return value


def base36_value(num):
    num = str(num)
    value = 0
    chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for i, c in enumerate(num[::-1]):
        value += chars.index(c) * 36 ** i
    return value


def replace_space_to_dash(text: str):
    return text.replace(" ", "-")


def replace_dot_to_dash(text: str):
    return text.replace(".", "-")


def replace_at_to_dash(text: str):
    return text.replace("@", "-")


def replace_space_dot_at_to_dash(text: str):
    text = text.replace(" ", "-")
    text = text.replace(".", "-")
    text = text.replace("@", "-")
    return text


def random_string(digits=4):
    return get_random_string(digits)


def get_substring_zero_to_find(text: str, char: str):
    return text[: text.find(char)]


def get_string(data, mode="string"):
    return data if data else ("" if mode == "string" else None)


def to_kebab_case(text):
    text = text.strip()
    if " " in text:
        return "-".join(text.lower().split())
    words = re.findall(r"[A-Z]?[a-z]+|[A-Z]+(?![a-z])", text)
    return "-".join(word.lower() for word in words)


def three_digit_separator(value):
    return "{:,}".format(value)


def three_digit_separator_without_decimal(value):
    return "{:,}".format(int(value))


def black_text(text):
    return set_text_color(text, TextColors.BLACK)


def red_text(text):
    return set_text_color(text, TextColors.RED)


def green_text(text):
    return set_text_color(text, TextColors.GREEN)


def yellow_text(text):
    return set_text_color(text, TextColors.YELLOW)


def blue_text(text):
    return set_text_color(text, TextColors.BLUE)


def magenta_text(text):
    return set_text_color(text, TextColors.MAGENTA)


def cyan_text(text):
    return set_text_color(text, TextColors.CYAN)


def white_text(text):
    return set_text_color(text, TextColors.WHITE)


def set_text_color(text, color="\033[0m"):
    return f"{color}{text}{TextColors.RESET}"


class PrintColored:
    def __init__(self):
        self.parts = []

    def add(self, text, color_func):
        self.parts.append(color_func(text))
        return self

    def add_black(self, text): self.parts.append(black_text(text))

    def add_red(self, text): self.parts.append(red_text(text))

    def add_green(self, text): self.parts.append(green_text(text))

    def add_yellow(self, text): self.parts.append(yellow_text(text))

    def add_blue(self, text): self.parts.append(blue_text(text))

    def add_magenta(self, text): self.parts.append(magenta_text(text))

    def add_cyan(self, text): self.parts.append(cyan_text(text))

    def add_white(self, text): self.parts.append(white_text(text))

    def build(self): return "".join(self.parts)

    def print(self):
        print(self.build())
