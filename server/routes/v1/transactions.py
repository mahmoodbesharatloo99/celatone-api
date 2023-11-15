from apiflask import APIBlueprint
from flask import jsonify, request
from utils.graphql.transactions import get_graphql_transactions

transactions_bp = APIBlueprint("transactions", __name__)


@transactions_bp.route("/<chain>/<network>/transactions", methods=["GET"])
def get_transactions(chain, network):
    try:
        limit = request.args.get("limit", type=int)
        if limit is None:
            raise ValueError("limit is required")
        offset = request.args.get("offset", type=int)
        if offset is None:
            raise ValueError("offset is required")
        is_wasm = request.args.get("is_wasm", False, type=bool)
        is_move = request.args.get("is_move", False, type=bool)

        data = get_graphql_transactions(chain, network, is_wasm, is_move, limit, offset)
        for tx in data.get("items", []):
            tx["signer"] = tx["account"]["address"]
            del tx["account"]
        data["total"] = data["latest"][0]["id"]
        del data["latest"]

        return data, 200
    except Exception as e:
        return jsonify(error=str(e)), 500
