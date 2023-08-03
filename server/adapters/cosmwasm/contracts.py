import json
from adapters.registry.registry import load_and_check_registry_data
from utils.graphql import get_contract_instantiator_admin


# contracts


def get_contracts(chain, network):
    contracts = load_and_check_registry_data(chain, network, "contracts")
    codes = load_and_check_registry_data(chain, network, "codes")
    contract_addresses = []
    for contract in contracts:
        contract_addresses.append(contract["address"])
    instantiator_admin_data = get_contract_instantiator_admin(
        chain, network, contract_addresses
    )
    code_map = {code["id"]: code for code in codes}
    instantiator_admin_map = {
        data["address"]: {
            "instantiator": data["instantiator"],
            "admin": data["admin"],
            "label": data["label"],
        }
        for data in instantiator_admin_data
    }
    for contract in contracts:
        if contract["code"] not in code_map:
            contract.update(
                {
                    "description": "",
                    "github": "",
                    **instantiator_admin_map.get(contract["address"], {}),
                }
            )
        else:
            code = code_map[contract["code"]]
            contract.update(
                {
                    "description": code["description"],
                    "github": code["github"],
                    **instantiator_admin_map.get(contract["address"], {}),
                }
            )
    return contracts


def get_contract(chain, network, contract_address):
    contracts = get_contracts(chain, network)
    contract = [
        contract for contract in contracts if contract["address"] == contract_address
    ][0]
    return contract
