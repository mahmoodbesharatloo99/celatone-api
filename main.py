from flask import Flask
import requests
import os

REGISTRY_URL = "https://cosmos-registry.alleslabs.dev/"

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


# Codes


@app.route("/<chain>/<network>/codes")
def get_codes(chain, network):
    codes = requests.get(f"{REGISTRY_URL}/data/{chain}/{network}/codes.json").json()
    return codes


@app.route("/<chain>/<network>/code/<code_id>")
def get_code(chain, network, code_id):
    codes = requests.get(f"{REGISTRY_URL}/data/{chain}/{network}/codes.json").json()
    code = [code for code in codes if code["id"] == code_id][0]
    return code


# Contracts


@app.route("/<chain>/<network>/contracts")
def get_contracts(chain, network):
    codes = requests.get(f"{REGISTRY_URL}/data/{chain}/{network}/contracts.json").json()
    return codes


@app.route("/<chain>/<network>/contract/<contract_address>")
def get_contract(chain, network, contract_address):
    contracts = requests.get(
        f"{REGISTRY_URL}/data/{chain}/{network}/contracts.json"
    ).json()
    contract = [
        contract for contract in contracts if contract["address"] == contract_address
    ][0]
    return contract


# Accounts


@app.route("/<chain>/<network>/accounts")
def get_accounts(chain, network):
    accounts = requests.get(
        f"{REGISTRY_URL}/data/{chain}/{network}/accounts.json"
    ).json()
    return accounts


@app.route("/<chain>/<network>/account/<account_address>")
def get_account(chain, network, account_address):
    accounts = requests.get(
        f"{REGISTRY_URL}/data/{chain}/{network}/accounts.json"
    ).json()
    account = [
        account for account in accounts if account["address"] == account_address
    ][0]
    return account


# Assets


@app.route("/<chain>/<network>/assets")
def get_addresses(chain, network):
    assets = requests.get(f"{REGISTRY_URL}/data/{chain}/{network}/assets.json").json()
    return assets


@app.route("/<chain>/<network>/assets/type/<asset_type>")
def get_asset_by_type(chain, network, asset_type):
    assets = requests.get(f"{REGISTRY_URL}/data/{chain}/{network}/assets.json").json()
    asset = [asset for asset in assets if asset["type"] == asset_type]
    return asset


@app.route("/<chain>/<network>/assets/slug/<asset_slug>")
def get_asset_by_slug(chain, network, asset_slug):
    assets = requests.get(f"{REGISTRY_URL}/data/{chain}/{network}/assets.json").json()
    asset = [asset for asset in assets if asset_slug in asset["slugs"]]
    return asset


@app.route("/<chain>/<network>/asset/<asset_id>")
def get_asset(chain, network, asset_id):
    assets = requests.get(f"{REGISTRY_URL}/data/{chain}/{network}/assets.json").json()
    asset = [asset for asset in assets if asset["id"] == asset_id][0]
    return asset


# Projects


@app.route("/<chain>/<network>/projects")
def get_projects(chain, network):
    projects = requests.get(
        f"{REGISTRY_URL}/data/{chain}/{network}/projects.json"
    ).json()
    return projects


@app.route("/<chain>/<network>/project/<project_id>")
def get_project(chain, network, project_id):
    projects = requests.get(
        f"{REGISTRY_URL}/data/{chain}/{network}/projects.json"
    ).json()
    project = [project for project in projects if project["slug"] == project_id][0]
    return project


# Entities


@app.route("/entities")
def get_entities():
    entities = requests.get(f"{REGISTRY_URL}/data/entities.json").json()
    return entities


@app.route("/entity/<entity_slug>")
def get_entity(entity_slug):
    entities = requests.get(f"{REGISTRY_URL}/data/entities.json").json()
    entity = [entity for entity in entities if entity["slug"] == entity_slug][0]
    return entity


# Balances


@app.route("/<chain>/<network>/balances/<account_address>")
def get_balances(chain, network, account_address):
    output_balances = []
    match chain:
        case "osmosis":
            match network:
                case "osmosis-1":
                    output_balances = get_native_balances(
                        "https://lcd.osmosis.zone/cosmos/bank/v1beta1/balances",
                        chain,
                        network,
                        account_address,
                    )
                case "osmo-test-4":
                    pass
        case "terra2":
            match network:
                case "phoenix-1":
                    output_balances = get_native_balances(
                        "https://phoenix-lcd.terra.dev/cosmos/bank/v1beta1/balances",
                        chain,
                        network,
                        account_address,
                    )
                case "pisco-1":
                    pass
    return output_balances


def get_native_balances(endpoint, chain, network, account_address):
    balances = requests.get(
        f"{endpoint}/{account_address}?pagination.limit=500"
    ).json()["balances"]
    supported_assets = requests.get(
        f"{REGISTRY_URL}/data/{chain}/{network}/assets.json"
    ).json()
    output_balance = []
    for balance in balances:
        if balance["denom"] in [asset["id"] for asset in supported_assets]:
            asset = [
                asset for asset in supported_assets if asset["id"] == balance["denom"]
            ][0]
            output_balance.append(
                {
                    "name": asset["name"],
                    "symbol": asset["symbol"],
                    "id": asset["id"],
                    "amount": balance["amount"],
                    "precision": asset["precision"],
                }
            )
    return output_balance


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
