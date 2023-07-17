from apiflask import APIBlueprint
from .service import IcnsService

service = IcnsService()

blueprint = APIBlueprint("ICNS", __name__, url_prefix="/icns")

@blueprint.route("/address/<name>/<bech32_prefix>", methods=["GET"])
def get_icns_address(name, bech32_prefix):
    return IcnsService.get_icns_address(name, bech32_prefix)


@blueprint.route("/names/<address>", methods=["GET"])
def get_icns_names(address):
    return IcnsService.get_icns_names(address)