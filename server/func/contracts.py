from func.registry import load_and_check_registry_data
from func.graphql import get_contract_instantiator_admin


def get_contracts(chain, network):
    contracts = []
    contracts = load_and_check_registry_data(chain, network, "contracts")
    codes = load_and_check_registry_data(chain, network, "codes")
    if len(contracts) > 0:
        instantiator_admin_data = get_contract_instantiator_admin(
            chain, network, [contract["address"] for contract in contracts]
        )
        for contract in contracts:
            if "description" not in contract or contract["description"] == "":
                code_description = [code["description"] for code in codes if code["id"] == contract["code"]][0]
                contract["description"] = code_description
            if "github" not in contract or contract["github"] == "":
                code_github = [code["github"] for code in codes if code["id"] == contract["code"]][0]
                contract["github"] = code_github
            for data in instantiator_admin_data:
                if contract["address"] == data["address"]:
                    contract["instantiator"] = data["instantiator"]
                    contract["admin"] = data["admin"]
                    contract["label"] = data["label"]
    return contracts


def get_contract(chain, network, contract_address):
    contracts = get_contracts(chain, network)
    contract = [contract for contract in contracts if contract["address"] == contract_address][0]
    return contract
