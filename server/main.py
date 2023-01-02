from flask import Flask
import os

import func.constants as constants
import func.codes as codes
import func.contracts as contracts
import func.accounts as accounts
import func.assets as assets
import func.projects as projects
import func.entities as entities
import func.balances as balances
import func.helper as helper

app = Flask(__name__)

# Root


@app.route("/")
def hello_world():
    return {"gm": "gm"}


# Codes


@app.route("/<chain>/<network>/codes")
def get_codes(chain, network):
    codes.get_codes(constants.REGISTRY_URL, chain, network)


@app.route("/<chain>/<network>/code/<code_id>")
def get_code(chain, network, code_id):
    codes.get_code(constants.REGISTRY_URL, chain, network, code_id)


# Contracts


@app.route("/<chain>/<network>/contracts")
def get_contracts(chain, network):
    contracts.get_contracts(constants.REGISTRY_URL, chain, network)


@app.route("/<chain>/<network>/contract/<contract_address>")
def get_contract(chain, network, contract_address):
    contracts.get_contract(constants.REGISTRY_URL, chain, network, contract_address)


# Accounts


@app.route("/<chain>/<network>/accounts")
def get_accounts(chain, network):
    accounts.get_accounts(constants.REGISTRY_URL, chain, network)


@app.route("/<chain>/<network>/account/<account_address>")
def get_account(chain, network, account_address):
    accounts.get_account(constants.REGISTRY_URL, chain, network, account_address)


# Assets


@app.route("/<chain>/<network>/assets")
def get_assets(chain, network):
    assets.get_assets(constants.REGISTRY_URL, chain, network)


@app.route("/<chain>/<network>/assets/type/<asset_type>")
def get_asset_by_type(chain, network, asset_type):
    assets.get_asset_by_type(constants.REGISTRY_URL, chain, network, asset_type)


@app.route("/<chain>/<network>/assets/slug/<asset_slug>")
def get_asset_by_slug(chain, network, asset_slug):
    assets.get_asset_by_slug(constants.REGISTRY_URL, chain, network, asset_slug)


@app.route("/<chain>/<network>/asset/<asset_id>")
def get_asset(chain, network, asset_id):
    assets.get_asset(constants.REGISTRY_URL, chain, network, asset_id)


# Projects


@app.route("/<chain>/<network>/projects")
def get_projects(chain, network):
    projects.get_projects(constants.REGISTRY_URL, chain, network)


@app.route("/<chain>/<network>/project/<project_id>")
def get_project(chain, network, project_id):
    projects.get_projects(constants.REGISTRY_URL, chain, network, project_id)


# Entities


@app.route("/entities")
def get_entities():
    entities.get_entities(constants.REGISTRY_URL)


@app.route("/entity/<entity_slug>")
def get_entity(entity_slug):
    entities.get_entity(constants.REGISTRY_URL, entity_slug)


# Balances


@app.route("/<chain>/<network>/balances/<account_address>")
def get_balances(chain, network, account_address):
    balances.get_balances(chain, network, account_address)


# Images


@app.route("/images/assets/<asset_symbol>")
def get_asset_image(asset_symbol):
    return helper.load_and_return_image("tokens", asset_symbol)


@app.route("/images/entities/<entity_slug>")
def get_entity_image(entity_slug):
    return helper.load_and_return_image("entites", entity_slug)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
