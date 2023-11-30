from statistics import median

from apiflask import APIBlueprint
from dateutil import parser
from utils.graphql import blocks, transactions

overviews_bp = APIBlueprint("overviews", __name__)


@overviews_bp.route("/<chain>/<network>/overviews/stats", methods=["GET"])
def get_overviews_stats(chain, network):
    try:
        data = transactions.get_graphql_latest_transaction_id(chain, network)
        latest_tx_id = data["latest"][0]["id"]
    except:
        latest_tx_id = None

    try:
        data = blocks.get_graphql_latest_block(chain, network)
        latest_block = data["latest"][0]
    except:
        latest_block = None

    try:
        data = blocks.get_graphql_block_times(chain, network)
        block_time = median(
            [
                (
                    parser.parse(b1["timestamp"]) - parser.parse(b2["timestamp"])
                ).total_seconds()
                for (b1, b2) in zip(data["blocks"][:100], data["blocks"][1:])
            ]
        )
    except:
        block_time = None

    return {
        "block_time": block_time,
        "latest_block": latest_block,
        "transaction_count": latest_tx_id,
    }
