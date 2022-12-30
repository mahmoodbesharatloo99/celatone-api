from flask import Flask
import requests
import os

app = Flask(__name__)

# Constants

REGISTRY_URL = "https://cosmos-registry.alleslabs.dev/"

LCD_DICT = {
    "osmosis": {
        "osmosis-1": "https://lcd.osmosis.zone",
        "osmo-test-4": "https://lcd-test.osmosis.zone",
    },
    "terra2": {
        "phoenix-1": "https://phoenix-lcd.terra.dev",
        "pisco-1": "https://pisco-lcd.terra.dev",
    },
}

HIVE_DICT = {
    "phoenix-1": "https://phoenix-hive.terra.dev",
    "pisco-1": "https://pisco-hive.terra.dev",
}

# Root


@app.route("/")
def hello_world():
    return {"gm": "gm"}


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
            output_balances = get_native_balances(
                f"{LCD_DICT[chain][network]}/cosmos/bank/v1beta1/balances",
                chain,
                network,
                account_address,
            )
        case "terra2":
            output_balances = get_native_balances(
                f"{LCD_DICT[chain][network]}/cosmos/bank/v1beta1/balances",
                chain,
                network,
                account_address,
            ) + get_hive_balance(chain, network, account_address)
    return output_balances


def split(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


def get_hive_balance(chain, network, account_address):
    supported_assets = get_asset_by_type(chain, network, "cw20")
    contract_addresses = [asset["id"] for asset in supported_assets]
    contract_address_chunks = split(contract_addresses, 50)
    output_balance = []
    for contract_address_chunk in contract_address_chunks:
        query = generate_hive_query(account_address, contract_address_chunk)
        hive_data = requests.post(
            f"{HIVE_DICT[network]}/graphql", json={"query": query}
        ).json()["data"]
        for contract_address, data in hive_data.items():
            if int(data["contractQuery"]["balance"]) > 0:
                asset = get_asset(chain, network, contract_address)
                output_balance.append(
                    {
                        "name": asset["name"],
                        "symbol": asset["symbol"],
                        "id": asset["id"],
                        "amount": data["contractQuery"]["balance"],
                        "precision": asset["precision"],
                    }
                )
    return output_balance


def generate_hive_query(account_address, contract_addresses):
    query = "query test {"
    for contract_address in contract_addresses:
        query += f"""
        {contract_address}: wasm{{
            contractQuery(contractAddress: "{contract_address}", query: {{
                balance: {{address : "{account_address}" }}
            }})
        }}
        """
    query += "}"
    return query


def get_native_balances(endpoint, chain, network, account_address):
    balances = requests.get(
        f"{endpoint}/{account_address}?pagination.limit=500"
    ).json()["balances"]
    supported_assets = get_asset_by_type(chain, network, "native")
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
