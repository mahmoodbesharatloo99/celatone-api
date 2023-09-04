import requests

import constants as constants
import adapters.core.assets as assets
import adapters.prices.prices as prices


def split(ls, n):
    return [ls[i : i + n] for i in range(0, len(ls), n)]


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
    supported_assets = assets.get_assets_by_type(chain, network, "cw20")
    asset_ids = [asset["id"] for asset in supported_assets if asset["coingecko"] != ""]
    print(asset_ids)
    asset_prices = prices.get_prices(chain, network, asset_ids)
    contract_addresses = [asset["id"] for asset in supported_assets]
    contract_address_chunks = split(contract_addresses, 50)
    for contract_address_chunk in contract_address_chunks:
        query = generate_hive_query(account_address, contract_address_chunk)
        hive_data = requests.post(
            f"{constants.HIVE_DICT[network]}/graphql", json={"query": query}
        ).json()["data"]
        output_balance += [
            {
                "name": asset["name"],
                "symbol": asset["symbol"],
                "id": asset["id"],
                "amount": data.get("contractQuery", {}).get("balance", 0),
                "precision": asset["precision"],
                "type": "cw20",
                "price": asset_prices.get(asset["id"], 0) if asset and asset["id"] in asset_prices else 0,
            }
            for asset, data in zip(
                supported_assets,
                [
                    hive_data.get(contract_address, {})
                    for contract_address in contract_address_chunk
                ],
            )
            if int(data.get("contractQuery", {}).get("balance", 0)) > 0
        ]
    return output_balance


def get_native_balances(endpoint, chain, network, account_address):
    balances = (
        requests.get(
            f"{endpoint}/cosmos/bank/v1beta1/balances/{account_address}?pagination.limit=500"
        )
        .json()
        .get("balances", [])
    )
    supported_assets = assets.get_assets_by_type(chain, network, "native")
    asset_ids = [asset["id"] for asset in supported_assets if asset["coingecko"] != ""]
    asset_prices = prices.get_prices(chain, network, asset_ids)
    output_balance = [
        {
            "name": asset["name"] if asset else None,
            "symbol": asset["symbol"] if asset else None,
            "id": balance["denom"],
            "amount": balance["amount"],
            "precision": asset["precision"] if asset else 0,
            "type": "native",
            "price": asset_prices.get(balance["denom"], 0)
            if asset and balance["denom"] in asset_prices
            else 0,
        }
        for balance in balances
        for asset in [
            next(
                (
                    asset
                    for asset in supported_assets
                    if asset["id"] == balance["denom"]
                ),
                None,
            )
        ]
    ]
    return output_balance
