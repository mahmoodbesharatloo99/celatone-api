from apiflask import APIBlueprint
from flask import jsonify, request
from utils.graphql.blocks import get_graphql_blocks

blocks_bp = APIBlueprint("blocks", __name__)


@blocks_bp.route("/<chain>/<network>/blocks", methods=["GET"])
def get_blocks(chain, network):
    try:
        limit = request.args.get("limit", type=int)
        if limit is None:
            raise ValueError("limit is required")
        offset = request.args.get("offset", type=int)
        if offset is None:
            raise ValueError("offset is required")

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
