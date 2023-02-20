import requests

import func.constants as constants
import func.assets as assets
import func.prices as prices


def split(ls, n):
    for i in range(0, len(ls), n):
        yield ls[i : i + n]


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
            if data is None or data["contractQuery"] is None:
                continue
            if int(data["contractQuery"]["balance"]) > 0:
                asset = assets.get_asset(chain, network, contract_address)
                output_balance.append(
                    {
                        "name": asset["name"],
                        "symbol": asset["symbol"],
                        "id": asset["id"],
                        "amount": data["contractQuery"]["balance"],
                        "precision": asset["precision"],
                        "type": "cw20",
                        "price": 1.00,
                    }
                )
    return output_balance


def get_native_balances(endpoint, chain, network, account_address):
    output_balance = []
    balances = requests.get(
        f"{endpoint}/cosmos/bank/v1beta1/balances/{account_address}?pagination.limit=500"
    )
    balances = balances.json()

    # Get all supported assets for this chain and network
    supported_assets = assets.get_assets_by_type(chain, network, "native")

    if "balances" in balances:
        for balance in balances["balances"]:
            # Check if the balance is a supported asset
            if balance["denom"] in [asset["id"] for asset in supported_assets]:
                asset = [
                    asset
                    for asset in supported_assets
                    if asset["id"] == balance["denom"]
                ][0]
                output_balance.append(
                    {
                        "name": asset["name"],
                        "symbol": asset["symbol"],
                        "id": asset["id"],
                        "amount": balance["amount"],
                        "precision": asset["precision"],
                        "type": "native",
                        "price": 1.00,
                    }
                )
            # If it's not a supported asset, just return the balance with no extra info
            else:
                output_balance.append(
                    {
                        "name": None,
                        "symbol": None,
                        "id": balance["denom"],
                        "amount": balance["amount"],
                        "precision": 0,
                        "type": "native",
                    }
                )
    return output_balance
