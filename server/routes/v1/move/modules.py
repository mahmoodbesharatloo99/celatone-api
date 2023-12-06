from adapters.move import pools
from apiflask import APIBlueprint
from utils.graphql.move.modules import get_graphql_modules
from utils.helper import get_query_param

modules_bp = APIBlueprint("modules", __name__)


@modules_bp.route("/<chain>/<network>/move/modules", methods=["GET"])
def get_move_modules(chain, network):
    limit = get_query_param("limit", type=int, required=True)
    offset = get_query_param("offset", type=int, required=True)

    data = get_graphql_modules(chain, network, limit, offset)
    for module in data.get("items", []):
        module["address"] = module["vm_address"]["accounts"][0]["address"]
        del module["vm_address"]

        module["block"] = module["module_histories"][0]["block"]
        del module["module_histories"]
        module["is_republished"] = (
            module["module_histories_aggregate"]["aggregate"]["count"] > 1
        )
        del module["module_histories_aggregate"]
    data["total"] = data["latest"][0]["id"]
    del data["latest"]

    return data
