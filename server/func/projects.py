import json
from func.registry import load_and_check_registry_data

from func.accounts import get_accounts
from func.assets import get_assets
from func.codes import get_codes
from func.contracts import get_contracts


def load_project_data(chain, network):
    accounts = get_accounts(chain, network)
    assets = get_assets(chain, network)
    codes = get_codes(chain, network)
    contracts = get_contracts(chain, network)
    return accounts, assets, codes, contracts


def load_project(entity, accounts, assets, codes, contracts):
    entity_dict = {}
    entity_dict["slug"] = entity["slug"]
    entity_dict["details"] = {
        "name": entity["name"],
        "description": entity["description"],
        "website": entity["website"],
        "github": entity["github"],
        "logo": f"https://celatone-api.alleslabs.dev/images/entities/{entity['slug']}",
        "socials": entity["socials"],
    }
    # only keep accounts for this entity
    relevant_accounts = [
        account for account in accounts if account["slug"] == entity["slug"]
    ]
    # only keep assets for this entity
    relevant_assets = [asset for asset in assets if entity["slug"] in asset["slugs"]]
    # only keep codes for this entity
    relevant_codes = [code for code in codes if code["slug"] == entity["slug"]]
    # only keep contracts for this entity
    relevant_contracts = [
        contract for contract in contracts if contract["slug"] == entity["slug"]
    ]
    if (
        len(relevant_accounts) != 0
        or len(relevant_codes) != 0
        or len(relevant_contracts) != 0
    ):
        entity_dict["accounts"] = relevant_accounts
        entity_dict["assets"] = relevant_assets
        entity_dict["codes"] = relevant_codes
        entity_dict["contracts"] = relevant_contracts
        return entity_dict
    return None


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
