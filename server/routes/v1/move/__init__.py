from apiflask import APIBlueprint

from . import modules, pools

move_bp = APIBlueprint("move", __name__)

move_bp.register_blueprint(modules.modules_bp)
move_bp.register_blueprint(pools.pools_bp)
