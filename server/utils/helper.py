import string
from flask import abort, request


def split(ls, n):
    return [ls[i : i + n] for i in range(0, len(ls), n)]


def get_query_param(
    name: str,
    type: type,
    default: any = None,
    required: bool = False,
):
    param = request.args.get(name)
    if param is None:
        if required:
            abort(400, f"{name} {type} is required")
        return default

    if type == bool:
        return param.lower() == "true"
    return type(param)


def validate_pagination_params(limit: int, offset: int):
    if limit < 0 or offset < 0:
        abort(400, "Limit and offset must be non-negative")


def is_graphql_timeout_error(e: Exception):
    return "canceling statement due to statement timeout" in str(e)


def is_txhash(txhash: str):
    return len(txhash) == 64 and all(c in string.hexdigits for c in txhash)
