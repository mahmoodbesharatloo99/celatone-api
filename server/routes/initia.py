from apiflask import APIBlueprint
from adapters.aldus.modules import ModuleManager

initia_bp = APIBlueprint("initia", __name__)


@initia_bp.route("/initia/modules/<chain>/<network>", methods=["GET"])
def get_modules(chain, network):
    """Get All Codes

    Returns a list of all the known codes based on the input chain and network
    """
    return ModuleManager(chain, network).get_modules()


@initia_bp.route("/initia/modules/<chain>/<network>/<address>/<name>", methods=["GET"])
def get_module(chain, network, address, name):
    """Get Code by ID

    Returns a specific code based on the input chain, network, and code_id
    """
    return ModuleManager(chain, network).get_module(address, name)
