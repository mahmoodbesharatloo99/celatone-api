from apiflask import APIBlueprint
from flask import abort
from utils.graphql.blocks import get_graphql_blocks
from utils.helper import get_query_param

blocks_bp = APIBlueprint("blocks", __name__)


@blocks_bp.route("/<chain>/<network>/blocks", methods=["GET"])
def get_blocks(chain, network):
    limit = get_query_param("limit", type=int, required=True)
    offset = get_query_param("offset", type=int, required=True)
    if limit < 0 or offset < 0:
        abort(400, "Limit and offset must be non-negative")

    data = get_graphql_blocks(chain, network, limit, offset)
    for block in data.get("items", []):
        block["transaction_count"] = block["transactions_aggregate"]["aggregate"][
            "count"
        ]
        del block["transactions_aggregate"]
    data["total"] = data["latest"][0]["height"]
    del data["latest"]

    return data
