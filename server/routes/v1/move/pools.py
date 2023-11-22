from adapters.move import pools
from apiflask import APIBlueprint

pools_bp = APIBlueprint("pools", __name__)


@pools_bp.route("/<chain>/<network>/move/pools", methods=["GET"])
def get_move_pools(chain, network):
    return pools.get_move_pools(chain, network)
