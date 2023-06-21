import json
from adapters.registry.registry import load_and_check_registry_data
from utils.graphql import get_contract_instantiator_admin


# contracts


def get_contracts(chain, network):
    contracts = load_and_check_registry_data(chain, network, "contracts")
    codes = load_and_check_registry_data(chain, network, "codes")
    if len(contracts) > 0:
        instantiator_admin_data = get_contract_instantiator_admin(
            chain, network, [contract["address"] for contract in contracts]
        )
        code_map = {code["id"]: code for code in codes}
        for contract in contracts:
            contract["description"] = code_map[contract["code"]]["description"]
            contract["github"] = code_map[contract["code"]]["github"]
            for data in instantiator_admin_data:
                if contract["address"] == data["address"]:
                    contract["instantiator"] = data["instantiator"]
                    contract["admin"] = data["admin"]
                    contract["label"] = data["label"]
    return contracts


def get_contract(chain, network, contract_address):
    contracts = get_contracts(chain, network)
    contract = [
        contract for contract in contracts if contract["address"] == contract_address
    ][0]
    return contract
