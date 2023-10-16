from flask import Blueprint
from adapters.cosmwasm import codes, contracts, helpers

cosmwasm_bp = Blueprint("cosmwasm", __name__)


@cosmwasm_bp.route("/codes/<chain>/<network>", methods=["GET"])
def get_codes(chain, network):
    """Get All Codes

    Returns a list of all the known codes based on the input chain and network
    """
    return codes.get_codes(chain, network)


@cosmwasm_bp.route("/codes/<chain>/<network>/<code_id>", methods=["GET"])
def get_code(chain, network, code_id):
    """Get Code by ID

    Returns a specific code based on the input chain, network, and code_id
    """
    return codes.get_code(chain, network, code_id)


@cosmwasm_bp.route("/contracts/<chain>/<network>", methods=["GET"])
def get_contracts(chain, network):
    """Get All Contracts

    Returns a list of all the known contracts based on the input chain and network"""
    return contracts.get_contracts(chain, network)


@cosmwasm_bp.route("/contracts/<chain>/<network>/<contract_address>", methods=["GET"])
def get_contract(chain, network, contract_address):
    """Get Get Contract by ID

    Returns a specific contract based on the input chain, network, and contract_address
    """
    return contracts.get_contract(chain, network, contract_address)


@cosmwasm_bp.route("/cosmwasm/<chain>/<network>/upload_access", methods=["GET"])
def get_upload_access(chain, network):
    """Get Upload Access

    Returns the upload access for the input chain and network"""
    return helpers.get_upload_access(chain, network)
