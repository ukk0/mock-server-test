import json
from typing import Optional

with open("mock_config.json") as config_file:
    config = json.load(config_file)


def determine_which_cassettes_to_use(expected_result: str) -> Optional[str]:
    valid_mocks = config["valid_mocks"]
    cassette_mappings = config.get("cassette_mappings", {})
    if expected_result not in valid_mocks:
        return None
    return cassette_mappings.get(expected_result)


def validate_that_requests_match(cassette, request_data):
    """
    Validates that the payload data for request is
    sufficiently identical to play a response from cassette.
    """
    assert request_data["method"] == cassette.requests[0].method
    assert request_data["path"] == cassette.requests[0].path
    request_data_json = json.loads(request_data["body"])
    cassette_data_json = json.loads(cassette.requests[0].body)
    request_keys = set(get_all_dict_keys(json_data=request_data_json))
    cassette_keys = set(get_all_dict_keys(json_data=cassette_data_json))
    assert cassette_keys.issubset(request_keys)


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
