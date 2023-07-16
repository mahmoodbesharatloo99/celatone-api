import os
import json


def load_asset_data(chain, network):
    global_assets_path = f"../registry/data/assets.json"
    if not os.path.exists(global_assets_path):
        return []
    with open(global_assets_path) as f:
        global_assets = json.load(f)
    assets = []
    for asset in global_assets:
        asset_id = asset["id"].get(chain, {}).get(network)
        if asset_id:
            asset["id"] = asset_id
            assets.append(asset)
    return assets


def load_and_check_registry_data(chain, network, content):
    path = f"../registry/data/{chain}/{network}/{content}.json"
    data = None
    if content == "assets":
        data = load_asset_data(chain, network)
    elif os.path.exists(path):
        with open(path) as f:
            data = json.load(f)
    return data or []

def load_project(entity, accounts, assets, codes, contracts):
    relevant_accounts = [
        account for account in accounts if account["slug"] == entity["slug"]
    ]
    relevant_assets = [asset for asset in assets if entity["slug"] in asset["slugs"]]
    relevant_codes = [code for code in codes if code["slug"] == entity["slug"]]
    relevant_contracts = [
        contract for contract in contracts if contract["slug"] == entity["slug"]
    ]
    if relevant_accounts or relevant_codes or relevant_contracts:
        return {
            "slug": entity["slug"],
            "details": {
                "name": entity["name"],
                "description": entity["description"],
                "website": entity["website"],
                "github": entity["github"],
                "logo": f"https://celatone-api.alleslabs.dev/images/entities/{entity['slug']}",
                "socials": entity["socials"],
            },
            "accounts": relevant_accounts,
            "assets": relevant_assets,
            "codes": relevant_codes,
            "contracts": relevant_contracts,
        }
    return None


def load_projects(accounts, assets, codes, contracts):
    entities = json.load(open(f"../registry/data/entities.json"))
    projects = []
    for entity in entities:
        entity_dict = load_project(entity, accounts, assets, codes, contracts)
        if entity_dict is not None:
            projects.append(entity_dict)
    return projects


def get_project(accounts, assets, codes, contracts, slug):
    entities = json.load(open(f"../registry/data/entities.json"))
    entity = [entity for entity in entities if entity["slug"] == slug][0]
    project = load_project(entity, accounts, assets, codes, contracts)
    if project is None:
        return []
    return project

def load_entities():
    with open("../registry/data/entities.json") as f:
        entities = json.load(f)
    return entities
