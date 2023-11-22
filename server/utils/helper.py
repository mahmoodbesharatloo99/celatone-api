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
