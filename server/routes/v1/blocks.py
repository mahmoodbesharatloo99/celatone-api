from apiflask import APIBlueprint
from flask import jsonify
from utils.graphql.blocks import get_graphql_blocks
from utils.helper import get_query_param

blocks_bp = APIBlueprint("blocks", __name__)


@blocks_bp.route("/<chain>/<network>/blocks", methods=["GET"])
def get_blocks(chain, network):
    try:
        limit = get_query_param("limit", type=int, required=True)
        offset = get_query_param("offset", type=int, required=True)

        data = get_graphql_blocks(chain, network, limit, offset)
        for block in data.get("items", []):
            block["transaction_count"] = block["transactions_aggregate"]["aggregate"][
                "count"
            ]
            del block["transactions_aggregate"]
        data["total"] = data["latest"][0]["height"]
        del data["latest"]

        return data, 200
    except Exception as e:
        return jsonify(error=str(e)), 500
