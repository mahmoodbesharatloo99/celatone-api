from apiflask import APIBlueprint
from flask import jsonify, request
from utils.graphql.transactions import get_graphql_transactions
from utils.helper import get_query_param

transactions_bp = APIBlueprint("transactions", __name__)


@transactions_bp.route("/<chain>/<network>/transactions", methods=["GET"])
def get_transactions(chain, network):
    try:
        limit = get_query_param("limit", type=int, required=True)
        offset = get_query_param("offset", type=int, required=True)
        is_wasm = get_query_param("is_wasm", type=bool, default=False)
        is_move = get_query_param("is_move", type=bool, default=False)

        data = get_graphql_transactions(chain, network, limit, offset, is_wasm, is_move)
        for tx in data.get("items", []):
            tx["signer"] = tx["account"]["address"]
            del tx["account"]
        data["total"] = data["latest"][0]["id"]
        del data["latest"]

        return data, 200
    except Exception as e:
        return jsonify(error=str(e)), 500
