import requests
import os
import shutil
from flask import send_file

import func.constants as constants
import func.assets as assets


def split(ls, n):
    for i in range(0, len(ls), n):
        yield ls[i : i + n]


def get_hive_balance(chain, network, account_address):
    output_balance = []
    supported_assets = assets.get_asset_by_type(chain, network, "cw20")
    contract_addresses = [asset["id"] for asset in supported_assets]
    contract_address_chunks = split(contract_addresses, 50)
    for contract_address_chunk in contract_address_chunks:
        query = generate_hive_query(account_address, contract_address_chunk)
        hive_data = requests.post(
            f"{constants.HIVE_DICT[network]}/graphql", json={"query": query}
        ).json()["data"]
        for contract_address, data in hive_data.items():
            if int(data["contractQuery"]["balance"]) > 0:
                asset = assets.get_asset(chain, network, contract_address)
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
    output_balance = []
    balances = requests.get(
        f"{endpoint}/{account_address}?pagination.limit=500"
    ).json()["balances"]
    supported_assets = assets.get_asset_by_type(chain, network, "native")
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


def load_and_return_image(image_type, image_name):
    if not os.path.exists("temp"):
        os.mkdir("temp")
    if not os.path.exists(f"temp/{image_name}.png"):
        image_res = requests.get(
            f"https://cosmos-registry.alleslabs.dev/assets/{image_type}/{image_name}.png",
            stream=True,
        )
        if image_res.status_code == 200:
            with open(f"temp/{image_name}.png", "wb") as f:
                shutil.copyfileobj(image_res.raw, f)
    return send_file(f"temp/{image_name}.png")
