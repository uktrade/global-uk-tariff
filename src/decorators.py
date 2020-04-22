from functools import wraps
from gzip import GzipFile
from io import BytesIO
from typing import Callable

from flask import Response, request


def cache_without_request_args(**defaults) -> Callable:
    """
    Cache responses for requests that either have no arguments, or have arguments matching the defaults.

    The backend is regularly handling and filtering through a large JSON file, but the majority
    of requests will be without filters - in which case the client is effectively asking for a static
    site. Caching these unfiltered pages functionally creates a static page in memory to be served
    to clients.
    """

    def decorator(func) -> Callable:
        responses = {}

        @wraps(func)
        def wrapper(*args, **kwargs) -> Response:
            for arg_name, arg_value in defaults.items():
                if request.args.get(arg_name, str(arg_value), type=str) != str(
                    arg_value
                ):
                    return func(*args, **kwargs)
            try:
                return responses[func.__name__]
            except KeyError:
                responses[func.__name__] = func(*args, **kwargs)

            return responses[func.__name__]

        return wrapper

    return decorator


def compress_response(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        response = func(*args, **kwargs)
        if not isinstance(response, Response):
            response = Response(response)

        # Check if the response is appropriate for gzipping.
        if (
            "gzip" not in request.headers.get("Accept-Encoding", "").lower()
            or not 200 <= response.status_code < 300
            or "Content-Encoding" in response.headers
        ):
            return response

        response.direct_passthrough = False
        # GZIP the response.
        gzip_buffer = BytesIO()
        with GzipFile(mode="wb", compresslevel=9, fileobj=gzip_buffer) as gzip_file:
            gzip_file.write(response.get_data())

        response.set_data(gzip_buffer.getvalue())
        response.headers["Content-Encoding"] = "gzip"
        response.direct_passthrough = False

        vary = response.headers.get("Vary")
        if vary:
            if "accept-encoding" not in vary.lower():
                response.headers["Vary"] = "{}, Accept-Encoding".format(vary)
        else:
            response.headers["Vary"] = "Accept-Encoding"
        return response

    return decorator
