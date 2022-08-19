from typing import Any

from apple.types.blockchain_format.program import Program


def json_to_applelisp(json_data: Any) -> Any:
    list_for_applelisp = []
    if isinstance(json_data, list):
        for value in json_data:
            list_for_applelisp.append(json_to_applelisp(value))
    else:
        if isinstance(json_data, dict):
            for key, value in json_data:
                list_for_applelisp.append((key, json_to_applelisp(value)))
        else:
            list_for_applelisp = json_data
    return Program.to(list_for_applelisp)
