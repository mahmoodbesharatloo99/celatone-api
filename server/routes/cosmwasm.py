from flask import Blueprint
from adapters.aldus.codes import CodeManager
from adapters.aldus.contracts import ContractManager
from adapters.aldus import helpers

cosmwasm_bp = Blueprint("cosmwasm", __name__)


@cosmwasm_bp.route("/codes/<chain>/<network>", methods=["GET"])
def get_codes(chain, network):
    """Get All Codes

    Returns a list of all the known codes based on the input chain and network
    """
    return CodeManager(chain, network).get_codes()


@cosmwasm_bp.route("/codes/<chain>/<network>/<code_id>", methods=["GET"])
def get_code(chain, network, code_id):
    """Get Code by ID

    Returns a specific code based on the input chain, network, and code_id
    """
    return CodeManager(chain, network).get_code(code_id)


@cosmwasm_bp.route("/contracts/<chain>/<network>", methods=["GET"])
def get_contracts(chain, network):
    """Get All Contracts

    Returns a list of all the known contracts based on the input chain and network"""
    return ContractManager(chain, network).get_contracts()


@cosmwasm_bp.route("/contracts/<chain>/<network>/<contract_address>", methods=["GET"])
def get_contract(chain, network, contract_address):
    """Get Get Contract by ID

    Returns a specific contract based on the input chain, network, and contract_address
    """
    return ContractManager(chain, network).get_contract(contract_address)


@cosmwasm_bp.route("/cosmwasm/<chain>/<network>/upload_access", methods=["GET"])
def get_upload_access(chain, network):
    """Get Upload Access

    Returns the upload access for the input chain and network"""
    return helpers.get_upload_access(chain, network)
