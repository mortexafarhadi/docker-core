def check_and_get_list(_list):
    return None if _list is None else _list if isinstance(_list, list) else _list


def sort_by_value_dict_ascending(_dict):
    return {k: v for k, v in sorted(_dict.items(), key=lambda item: item[1])}


def sort_by_value_dict_descending(_dict):
    return {
        k: v for k, v in sorted(_dict.items(), key=lambda item: item[1], reverse=True)
    }
