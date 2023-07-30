import os
import json
from .graphql import get_graphql_code_details


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

def load_codes(chain, network):
    codes = []
    path = f"../registry/data/{chain}/{network}/codes.json"
    if os.path.exists(path):
        with open(path) as f:
            codes = json.load(f)

    code_ids = []
    for code in codes:
        code_ids.append(code["id"])

    graphql_details = get_graphql_code_details(chain, network, code_ids)

    graphql_map = {}
    for detail in graphql_details:
        graphql_map[detail["code_id"]] = detail

    for code in codes:
        if code["id"] not in graphql_map:
            print(f"{chain}-{network}: code detail for id: {code['id']} is not found")
            continue
        code_details = graphql_map[code["id"]]
        code.update(
            {
                "cw2Contract": code_details["cw2_contract"],
                "cw2Version": code_details["cw2_version"],
                "uploader": code_details["creator"],
                "contracts": code_details["contract_instantiated"],
                "instantiatePermission": code_details["access_config_permission"],
                "permissionAddresses": code_details["access_config_addresses"],
            }
        )

    return codes

def get_project(accounts, assets, codes, contracts, slug):
    entities = json.load(open(f"../registry/data/entities.json"))
    entity = [entity for entity in entities if entity["slug"] == slug]
    if len(entity) == 0: return []
    
    project = load_project(entity[0], accounts, assets, codes, contracts)
    if project is None:
        return []
    return project

