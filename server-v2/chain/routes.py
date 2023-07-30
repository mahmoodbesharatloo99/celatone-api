from apiflask import APIBlueprint
from .service import ChainService

service = ChainService()

blueprint = APIBlueprint("chain", __name__, url_prefix="/chains")

@blueprint.route("", methods=["GET"])
def chains():
    return service.chains

## TODO: Handler Chain not found error
@blueprint.route("/<name>", methods=["GET"])
def chainByName(name: str) :
    return service.get_chain(name)

