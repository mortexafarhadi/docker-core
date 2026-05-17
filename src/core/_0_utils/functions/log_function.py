def insert_query_text_log(model_name, obj):
    """Generate INSERT query text for logging purposes"""
    if obj is None:
        return f"INSERT INTO {model_name} => [Object data not available]"

    res = f"INSERT INTO {model_name} => "
    field_values = []

    for field in obj._meta.fields:
        field_name = field.name
        field_value = getattr(obj, field_name, None)
        field_values.append(f"{field_name}: {field_value}")

    res += ", ".join(field_values)
    return res
