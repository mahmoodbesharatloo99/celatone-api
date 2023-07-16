from apiflask import APIBlueprint
from .service import ChainService

service = ChainService()

blueprint = APIBlueprint("chain", __name__)

@blueprint.route("/chains", methods=["GET"])
def chains():
    return service.chains

@blueprint.route("/chain/<name>", methods=["GET"])
def chainByName(name: str) :
    return service.get_chain(name)

