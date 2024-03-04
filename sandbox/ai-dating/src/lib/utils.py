from collections.abc import Callable
from functools import wraps
from typing import Any, Optional

from flask import request

def _camel_case_to_snake_case(string: str) -> str:
    import re

    string = string.replace(".", "_")
    # 'HTTPResponseCode' -> 'HTTP_ResponseCode'
    string = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", string)
    # 'HTTP_ResponseCode' -> 'HTTP_Response_Code'
    string = re.sub("([a-z0-9])([A-Z])", r"\1_\2", string)
    # 'HTTP_Response_Code' -> 'http_response_code
    return string.lower()

def request_fields(
    required_fields: set,
    optional_fields: Optional[set] = None,
    params_dict_getter: Callable = lambda request: request.json,
) -> Callable:
    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def decorated_function(*args: Any, **kwargs: Any) -> Any:
            request_params = params_dict_getter(request)
            missing_fields = required_fields - request_params.keys()
            extra_fields = request_params.keys() - required_fields - (optional_fields or set())
            if len(missing_fields) > 0:
                raise Exception(f"Missing required fields: {', '.join(sorted(missing_fields))}")
            if len(extra_fields) > 0:
                raise Exception(f"Extraneous fields included: {', '.join(sorted(extra_fields))}")

            kwargs.update(
                {_camel_case_to_snake_case(param): request_params[param] for param in request_params}
            )

            return f(*args, **kwargs)

        return decorated_function

    return decorator