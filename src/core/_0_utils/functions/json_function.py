import os

import json
from _0_utils.base_variables import BASE_DIR
from _0_utils.functions.string_function import bytes_to_text


def str_to_json(text: str):
    return json.loads(text)


def byte_to_json(byte_str: bytes):
    return str_to_json(bytes_to_text(byte_str))


def read_json(file_path, default=None):
    try:
        _file_path = os.path.join(BASE_DIR, file_path)
        if not os.path.exists(_file_path):
            raise FileNotFoundError(f"Configuration file not found: {_file_path}")
        with open(_file_path, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error in load File{e}")
        return default
