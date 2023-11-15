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

        graphql_res = get_graphql_blocks(chain, network, limit, offset)
        return {
            "items": [
                {
                    "hash": item["hash"],
                    "height": item["height"],
                    "timestamp": item["timestamp"],
                    "transaction_count": item["transactions_aggregate"]["aggregate"][
                        "count"
                    ],
                    "validator": item["validator"],
                }
                for item in graphql_res["blocks"]
            ],
            "total": graphql_res["latest"][0]["height"],
        }, 200
    except Exception as e:
        print("errorrrr", e)
        return jsonify(error=str(e)), 500
