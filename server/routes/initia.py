from apiflask import APIBlueprint
from adapters.aldus.modules import MoveModuleManager

initia_bp = APIBlueprint("initia", __name__)


@initia_bp.route("/<chain>/<network>/move_modules", methods=["GET"])
def get_move_modules(chain, network):
    """Get All Codes

    Returns a list of all the known codes based on the input chain and network
    """
    return MoveModuleManager(chain, network).get_move_modules()


@initia_bp.route("/<chain>/<network>/move_modules/<address>/<name>", methods=["GET"])
def get_move_module(chain, network, address, name):
    """Get Code by ID

    Returns a specific code based on the input chain, network, and code_id
    """
    return MoveModuleManager(chain, network).get_move_module(address, name)
