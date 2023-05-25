from func.registry import load_and_check_registry_data
from func.graphql import get_contract_instantiator_admin


def get_contracts(chain, network):
    contracts = load_and_check_registry_data(chain, network, "contracts")
    codes = load_and_check_registry_data(chain, network, "codes")
    code_descriptions = {code["id"]: code["description"] for code in codes}
    code_githubs = {code["id"]: code["github"] for code in codes}
    instantiator_admin_data = get_contract_instantiator_admin(
        chain, network, [contract["address"] for contract in contracts]
    )
    contract_data = {data["address"]: data for data in instantiator_admin_data}
    for contract in contracts:
        contract["description"] = code_descriptions.get(contract["code"], "")
        contract["github"] = code_githubs.get(contract["code"], "")
        data = contract_data.get(contract["address"], {})
        contract["instantiator"] = data.get("instantiator", "")
        contract["admin"] = data.get("admin", "")
        contract["label"] = data.get("label", "")
        contract["imageUrl"] = f"https://celatone-api.alleslabs.dev/images/entities/{contract['slug']}"
    return contracts


def get_contract(chain, network, contract_address):
    contracts = get_contracts(chain, network)
    contract = [contract for contract in contracts if contract["address"] == contract_address][0]
    return contract
