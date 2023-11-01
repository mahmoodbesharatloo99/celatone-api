from adapters.aldus import accounts, assets, codes, contracts, modules
from utils.aldus import get_aldus_entities_data
from utils.constants import ALDUS_URL
from utils.images import get_image


def load_project_data(chain, network):
    loaded_accounts = accounts.AccountManager(chain, network).get_accounts()
    loaded_assets = assets.AssetManager(chain, network).get_assets()
    loaded_codes = codes.CodeManager(chain, network).get_codes()
    loaded_contracts = contracts.ContractManager(chain, network).get_contracts()
    loaded_modules = []
    if chain == "initia":
        loaded_modules = modules.MoveModuleManager(chain, network).get_move_modules()
    return loaded_accounts, loaded_assets, loaded_codes, loaded_contracts, loaded_modules


def load_project(entity, accounts, assets, codes, contracts, modules):
    relevant_accounts = [account for account in accounts if account["slug"] == entity["slug"]]
    relevant_assets = [asset for asset in assets if entity["slug"] in asset["slugs"]]
    relevant_codes = [code for code in codes if code["slug"] == entity["slug"]]
    relevant_contracts = [contract for contract in contracts if contract["slug"] == entity["slug"]]
    relevant_modules = [module for module in modules if module["slug"] == entity["slug"]]
    if relevant_accounts or relevant_codes or relevant_contracts or relevant_modules:
        return {
            "slug": entity["slug"],
            "details": {
                "name": entity["name"],
                "description": entity["description"],
                "website": entity["website"],
                "github": entity["github"],
                "logo": get_image(f"{ALDUS_URL}/assets/entities/{entity['slug']}"),
                "socials": entity["socials"],
            },
            "accounts": relevant_accounts,
            "assets": relevant_assets,
            "codes": relevant_codes,
            "contracts": relevant_contracts,
            "modules": relevant_modules,
        }
    return None


def load_projects(chain, network):
    entities = get_aldus_entities_data()
    accounts, assets, codes, contracts, modules = load_project_data(chain, network)
    projects = []
    for entity in entities:
        entity_dict = load_project(entity, accounts, assets, codes, contracts, modules)
        if entity_dict is not None:
            projects.append(entity_dict)
    return projects


def get_projects(chain, network):
    projects = load_projects(chain, network)
    return projects


def get_project(chain, network, slug):
    accounts, assets, codes, contracts, modules = load_project_data(chain, network)
    entities = get_aldus_entities_data()
    entity = [entity for entity in entities if entity["slug"] == slug][0]
    project = load_project(entity, accounts, assets, codes, contracts, modules)
    if project is None:
        return []
    return project
