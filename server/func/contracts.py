import json
import os
from func.registry import load_and_check_registry_data


def get_contracts(chain, network):
    contracts = load_and_check_registry_data(chain, network, "contracts")
    return contracts


def get_contract(chain, network, contract_address):
    contracts = load_and_check_registry_data(chain, network, "contracts")
    contract = [
        contract for contract in contracts if contract["address"] == contract_address
    ][0]
    return contract
