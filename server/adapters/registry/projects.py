import json

from adapters.core import accounts, assets
from adapters.cosmwasm import codes, contracts


def load_project_data(chain, network):
    loaded_accounts = accounts.get_accounts(chain, network)
    loaded_assets = assets.get_assets(chain, network)
    loaded_codes = codes.get_codes(chain, network)
    loaded_contracts = contracts.get_contracts(chain, network)
    return loaded_accounts, loaded_assets, loaded_codes, loaded_contracts


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
    relevant_accounts = list(
        filter(lambda account: account["slug"] == entity["slug"], accounts)
    )
    # only keep assets for this entity
    relevant_assets = list(
        filter(lambda asset: entity["slug"] in asset["slugs"], assets)
    )
    # only keep codes for this entity
    relevant_codes = list(filter(lambda code: code["slug"] == entity["slug"], codes))
    # only keep contracts for this entity
    relevant_contracts = list(
        filter(lambda contract: contract["slug"] == entity["slug"], contracts)
    )
    if any([relevant_codes, relevant_contracts, relevant_accounts]):
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
