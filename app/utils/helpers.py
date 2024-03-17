def get_all_dict_keys(json_data, parent_key=None) -> list:
    """
    Extracts all the keys from dictionaries, including nested
    dictionaries.
    """
    keys = []
    if isinstance(json_data, dict):
        for key, value in json_data.items():
            current_key = f"{parent_key}.{key}" if parent_key else key
            if isinstance(value, dict):
                keys.extend(get_all_dict_keys(value, current_key))
            else:
                keys.append(current_key)
    return keys
