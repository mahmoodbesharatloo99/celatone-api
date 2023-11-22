from apiflask import APIBlueprint

from . import pools

move_bp = APIBlueprint("move", __name__)

move_bp.register_blueprint(pools.pools_bp)
