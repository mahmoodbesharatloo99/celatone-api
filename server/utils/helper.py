from flask import abort, request


def split(ls, n):
    return [ls[i : i + n] for i in range(0, len(ls), n)]


def get_query_param(
    name: str,
    type: type,
    default: any = None,
    required: bool = False,
):
    param = request.args.get(name, default, type=type)
    if required and param is None:
        abort(400, f"{name} {type} is required")
    return param
