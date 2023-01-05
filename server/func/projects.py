import json
from func.registry import load_and_check_registry_data


def load_project_data(chain, network):
    accounts = load_and_check_registry_data(chain, network, "accounts")
    assets = load_and_check_registry_data(chain, network, "assets")
    codes = load_and_check_registry_data(chain, network, "codes")
    contracts = load_and_check_registry_data(chain, network, "contracts")
    return accounts, assets, codes, contracts


def load_project(entity, accounts, assets, codes, contracts):
    entity_dict = {}
    relevant_accounts = [
        account for account in accounts if account["slug"] == entity["slug"]
    ]
    relevant_assets = [asset for asset in assets if entity["slug"] in asset["slugs"]]
    relevant_codes = [code for code in codes if code["slug"] == entity["slug"]]
    relevant_contracts = [
        contract for contract in contracts if contract["slug"] == entity["slug"]
    ]
    if len(relevant_codes) == 0 and len(relevant_contracts) == 0:
        return None
    entity_dict["slug"] = entity["slug"]
    entity_dict["details"] = {
        "name": entity["name"],
        "description": entity["description"],
        "website": entity["website"],
        "github": entity["github"],
        "logo": f"https://celatone-api.alleslabs.dev/images/entities/{entity['slug']}",
        "socials": entity["socials"],
    }
    entity_dict["accounts"] = relevant_accounts
    entity_dict["assets"] = relevant_assets
    entity_dict["codes"] = relevant_codes
    entity_dict["contracts"] = relevant_contracts
    return entity_dict


def load_projects(chain, network):
    entities = json.load(open(f"../registry/data/entities.json"))
    accounts, assets, codes, contracts = load_project_data(chain, network)
    projects = []
    for entity in entities:
        entity_dict = load_project(entity, accounts, assets, codes, contracts)
        if entity_dict is not None:
            projects.append(entity_dict)
    return projects


def get_projects(chain, network):
    projects = load_projects(chain, network)
    return projects


def get_project(chain, network, slug):
    accounts, assets, codes, contracts = load_project_data(chain, network)
    entities = json.load(open(f"../registry/data/entities.json"))
    entity = [entity for entity in entities if entity["slug"] == slug][0]
    project = load_project(entity, accounts, assets, codes, contracts)
    if project is None:
        return []
    return project
