from flask import Blueprint
from adapters.icns import resolver

icns_bp = Blueprint("icns", __name__)


@icns_bp.route("/icns/address/<name>/<bech32_prefix>", methods=["GET"])
def get_icns_address(name, bech32_prefix):
    return resolver.get_icns_address(name, bech32_prefix)


@icns_bp.route("/icns/names/<address>", methods=["GET"])
def get_icns_names(address):
    return resolver.get_icns_names(address)
