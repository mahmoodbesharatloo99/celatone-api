from apiflask import APIBlueprint
from utils.graphql.move.modules import (
    get_graphql_module_id,
    get_graphql_module_txs,
    get_graphql_modules,
)
from utils.helper import get_query_param, validate_pagination_params

modules_bp = APIBlueprint("modules", __name__)


@modules_bp.route("/<chain>/<network>/move/modules", methods=["GET"])
def get_move_modules(chain, network):
    limit = get_query_param("limit", type=int, required=True)
    offset = get_query_param("offset", type=int, required=True)
    validate_pagination_params(limit, offset)

    data = get_graphql_modules(chain, network, limit, offset)
    for module in data.get("items", []):
        module["address"] = module["vm_address"]["accounts"][0]["address"]
        del module["vm_address"]

        module["block"] = module["module_histories"][0]["block"]
        del module["module_histories"]
        module["is_republish"] = (
            module["module_histories_aggregate"]["aggregate"]["count"] > 1
        )
        del module["module_histories_aggregate"]
    data["total"] = data["latest"][0]["id"]
    del data["latest"]

    return data


@modules_bp.route(
    "/<chain>/<network>/move/modules/<vm_address>/<name>/txs", methods=["GET"]
)
def get_move_module_txs(chain, network, vm_address, name):
    limit = get_query_param("limit", type=int, required=True)
    offset = get_query_param("offset", type=int, required=True)
    is_initia = get_query_param("is_initia", type=bool, default=False)
    validate_pagination_params(limit, offset)

    module_id = get_graphql_module_id(chain, network, vm_address, name)
    if module_id is None:
        return {"items": [], "total": 0}

    data = get_graphql_module_txs(chain, network, module_id, limit, offset, is_initia)
    for tx in data.get("items", []):
        tx["height"] = tx["block"]["height"]
        tx["created"] = tx["block"]["timestamp"]
        tx["hash"] = tx["transaction"]["hash"]
        tx["messages"] = tx["transaction"]["messages"]
        tx["sender"] = tx["transaction"]["account"]["address"]
        tx["success"] = tx["transaction"]["success"]
        tx["is_send"] = tx["transaction"]["is_send"]
        tx["is_ibc"] = tx["transaction"]["is_ibc"]
        tx["is_move_publish"] = tx["transaction"]["is_move_publish"]
        tx["is_move_upgrade"] = tx["transaction"]["is_move_upgrade"]
        tx["is_move_execute"] = tx["transaction"]["is_move_execute"]
        tx["is_move_script"] = tx["transaction"]["is_move_script"]

        if is_initia:
            tx["is_opinit"] = tx["transaction"]["is_opinit"]

        del tx["block"]
        del tx["transaction"]
    data["total"] = data["module_transactions_aggregate"]["aggregate"]["count"]
    del data["module_transactions_aggregate"]

    return data
